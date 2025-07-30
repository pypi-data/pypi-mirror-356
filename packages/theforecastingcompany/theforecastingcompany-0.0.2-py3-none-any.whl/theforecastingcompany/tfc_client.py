import datetime as dt
import os
from typing import Any, Optional

import httpx
import pandas as pd

from .utils import TFCModels, cross_validate_single_model


class TFCClient:
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        max_concurrent: int = 200,
        max_tries: int = 5,
    ):
        self.base_url = base_url
        self.api_key = api_key if api_key else os.getenv("TFC_API_KEY", None)
        self.max_concurrent = max_concurrent
        self.max_tries = max_tries
        if self.api_key is None:
            raise ValueError("No API key provided")

    def _handle_response(self, response: httpx.Response) -> dict[str, Any]:
        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            error_body = exc.response.text
            if exc.response.status_code == 400:
                raise TFCBadRequestError(
                    "Bad request. Check your input parameters.",
                    status_code=400,
                    response_body=error_body,
                ) from exc
            elif exc.response.status_code == 401:
                raise TFCUnauthorizedError(
                    "Unauthorized. Check your API key.",
                    status_code=401,
                    response_body=error_body,
                ) from exc
            elif exc.response.status_code == 403:
                raise TFCForbiddenError(
                    "Forbidden. You don't have permission to access this resource.",
                    status_code=403,
                    response_body=error_body,
                ) from exc
            elif exc.response.status_code == 404:
                raise TFCNotFoundError("Resource not found.", status_code=404, response_body=error_body) from exc
            elif exc.response.status_code == 422:
                raise TFCUnprocessableEntityError(
                    "Unprocessable entity. Check your request data.",
                    status_code=422,
                    response_body=error_body,
                ) from exc
            elif 500 <= exc.response.status_code < 600:
                raise TFCServerError(
                    f"Server error: {exc.response.status_code}",
                    status_code=exc.response.status_code,
                    response_body=error_body,
                ) from exc
            else:
                raise TFCAPIError(
                    f"Unexpected error: {exc.response.status_code}",
                    status_code=exc.response.status_code,
                    response_body=error_body,
                ) from exc

        try:
            return response.json()
        except ValueError as exc:
            raise TFCAPIError("Invalid JSON in response body", response_body=response.text) from exc

    def _validate_inputs(
        self,
        train_df: pd.DataFrame,
        future_df: pd.DataFrame | None,
        future_variables: list[str],
        static_variables: list[str],
        hist_variables: list[str],
        id_col: str,
        date_col: str,
    ) -> None:
        if any(not isinstance(arg, list) for arg in [future_variables, static_variables, hist_variables]):
            raise ValueError("Future, static and historical variables should be lists of columns names.")

        if future_df is not None:
            # TODO: Add checks in TFCModels to make sure only supported variables are provided.
            # TODO: static variables don't need to be stored in the future_df, unless I want to predict new items (in which case at leats the mapping should be provided).
            if not all(col in future_df.columns for col in future_variables):
                raise ValueError("All future variables must be present in future_df")
            static_in_future = [col for col in static_variables if col in future_df.columns if col != id_col]
            # If not static feature is in future_df: I will predict for all items in train_df
            # If I have ALL static features in future_df, I will only predict for the items in there.
            if len(static_in_future) > 0 and not all(col in future_df.columns for col in static_variables):
                raise ValueError(
                    "Missing static variables in future_df:",
                    [col for col in static_variables if col not in future_df.columns],
                )

        # TODO: Add support for static variables (not yet supported by TFC) and historical variables (need to populate them in send_async_requests).
        if train_df.groupby(id_col).agg(last_date=(date_col, "max"))["last_date"].unique().shape[0] > 1:
            raise ValueError("All series must have the same last date")
        if len(set(future_variables)) != len(future_variables):
            raise ValueError("Future variables contain duplicates")
        if len(set(static_variables)) != len(static_variables):
            raise ValueError("Static variables contain duplicates")
        if len(set(hist_variables)) != len(hist_variables):
            raise ValueError("Historical variables contain duplicates")
        if len(set(future_variables + static_variables + hist_variables)) != len(
            future_variables + static_variables + hist_variables
        ):
            raise ValueError("Future, static and historical variables contain duplicates")
        if future_df is None and future_variables:
            raise ValueError("Future variables provided but no future_df provided")

    def make_future_df(
        self,
        train_df: pd.DataFrame,
        freq: str,
        horizon: int,
        future_df: pd.DataFrame | None = None,
        id_col: str = "unique_id",
        date_col: str = "ds",
        future_variables: list[str] | None = None,
        static_variables: list[str] | None = None,
    ) -> pd.DataFrame:
        """Helper function to generate the indexes and static features for the future_df.

        Args:
            train_df (pd.DataFrame): Dataframe with historical target and features' values.
            freq (str): Frequency Alias of the time series, e.g., H, D, W, M, Q, Y.
            horizon (int): Number of steps to forecast.
            future_df (pd.DataFrame | None, optional): Dataframe with future target and features' values. Defaults to None.
            id_col (str, optional): Column name in train_df and future_df containing the unique identifier of each time series. Defaults to "unique_id".
            date_col (str, optional): Column name in train_df and future_df containing the date of each time series. Defaults to "ds".
            future_variables (list[str], optional): Future variables to be used by the model. Defaults to []. If future_variables are provided,
            this method is used to add the static variables to the future_df, if not already present.
            static_variables (list[str], optional): Static variables to be used by the model. Defaults to [].

        Returns:
            pd.DataFrame: Dataframe with all unique_id to be forecasted, corresponding static features and future_variables.
        """
        if static_variables is None:
            static_variables = []
        if future_variables is None:
            future_variables = []
        # 1. Future_df is None: build future_df with all static features from unique_id in train_df
        # 2. Future_df is not None and all static_variables (beside id_col) are in future_df: do not merge static features,
        # and only predict for items in future_df (will raise error if the method does not support new static_variables)
        # 3. Future_df is not None and not all static_variables (beside id_col) are in future_df: merge static features. It cannot
        # be that only some static variables are in future_df, as this would raise an error in _validate_input().
        static_feat_cols = [id_col] + [col for col in static_variables if col != id_col]
        static_feat_df = train_df[static_feat_cols].drop_duplicates(keep="last")

        # Future_df is None: predict for all training items, no future_variables
        # TODO: currently static features are handles as future_variables
        if future_df is None:
            assert len(future_variables) == 0, "Future variables provided but no future_df provided"
            myfreq = "7D" if freq == "W" else freq
            start_fc_date = train_df[date_col].max() + pd.tseries.frequencies.to_offset(myfreq)
            dates_df = pd.DataFrame(
                pd.date_range(start=start_fc_date, periods=horizon, freq=myfreq),
                columns=[date_col],
            )
            future_df = pd.merge(dates_df, static_feat_df, how="cross")

            return future_df
        else:
            nb_steps = future_df.groupby(id_col).agg(steps=(date_col, "count"))["steps"].unique()
            assert len(nb_steps) == 1 and nb_steps[0] >= horizon, (
                "All items in future_df must have one row per date in the horizon."
            )

        # Future_df is not None, only future_variables: predict for all items in future_df
        # id_col always in future_df. Thus I check len() > 1
        if len(static_feat_cols) > 1 and not all(col in future_df.columns for col in static_feat_cols):
            future_df = future_df.merge(static_feat_df, on=id_col, how="left")

        return future_df

    def forecast(
        self,
        train_df: pd.DataFrame,
        model: TFCModels,
        horizon: int,
        freq: str,
        add_holidays: bool = False,
        add_events: bool = False,
        country_isocode: str | None = None,
        future_df: pd.DataFrame | None = None,
        future_variables: list[str] | None = None,
        historical_variables: list[str] | None = None,
        static_variables: list[str] | None = None,
        id_col: str = "unique_id",
        date_col: str = "ds",
        target_col: str = "target",
    ) -> pd.DataFrame:
        """Given a context dataframe train_df, compute forecast over the specified horizon.

        Args:
            train_df (pd.DataFrame): Context dataframe, containing history for all time series to be predicted.
            model (TFCModels): Model to be used for forecasting. See https://api.retrocast.com/docs/routes/index for a list of model
            identifiers. You can also use the tfc_client.utils.TFCModels enum.
            horizon (int): Number of steps to forecast.
            freq (str): Frequency Alias of the time series, e.g., H, D, W, M, Q, Y.
            add_holidays (bool, optional): Whether to include TFC-holidays as features. Defaults to False.
            add_events (bool, optional): Whether to include TFC-events as features. Defaults to False.
            country_isocode (str | None, optional): ISO (eg, US, GB,..) code of the country for which the forecast is requested. This is used for fetching the right
            holidays and events. Defaults to None.
            future_df (pd.DataFrame | None, optional): Future dataframe. Defaults to None. Should contain all the future_variables needed to forecast.
            future_variables (list[str] | None, optional): Future variables to be used by the model. Defaults to None.
            historical_variables (list[str] | None, optional): Historical variables to be used by the model. Defaults to None.
            static_variables (list[str] | None, optional): Static variables to be used by the model. Defaults to None.
            id_col (str, optional): Column name in train_df and future_df containing the unique identifier of each time series. Defaults to "unique_id".
            date_col (str, optional): Column name in train_df and future_df containing the date of each time series. Defaults to "ds".
            target_col (str, optional): Column name in train_df containing the target of each time series. Defaults to "target".

        Returns:
            pd.DataFrame: Forecast dataframe, containing the forecast for all time series.
        """
        max_train_date = train_df[date_col].max()
        # TODO: Find better fix.
        myfreq = "7D" if freq == "W" else freq
        max_fc_date = max_train_date + pd.tseries.frequencies.to_offset(myfreq)
        fcds = [max_fc_date]
        if future_variables is None:
            future_variables = []
        if static_variables is None:
            static_variables = []
        if historical_variables is None:
            historical_variables = []
        self._validate_inputs(
            train_df,
            future_df,
            future_variables,
            static_variables,
            historical_variables,
            id_col=id_col,
            date_col=date_col,
        )
        # Add static variables if necessary
        # Build future_df is this is None
        future_df = self.make_future_df(
            train_df,
            freq,
            horizon,
            future_df,
            id_col,
            date_col,
            future_variables,
            static_variables,
        )
        # Fill Targets and Historical variables with 0 for the future. These values won't be used thanks to te FCD index.
        future_df = pd.DataFrame(
            future_df.assign(**{col: 0 for col in train_df.columns if col not in future_df.columns})[
                train_df.columns
            ]  # Make sure to have the same column order
        )
        full_df = pd.concat([train_df, future_df], axis=0)

        return cross_validate_single_model(
            full_df,
            fcds,
            model,
            horizon,
            freq,
            add_holidays,
            add_events,
            country_isocode,
            future_variables,
            historical_variables,
            static_variables,
            self.max_concurrent,
            self.max_tries,
            self.api_key,
            self.base_url,
            id_col,
            date_col,
            target_col,
        )

    def cross_validate(
        self,
        train_df: pd.DataFrame,
        fcds: list[dt.date | dt.datetime],
        model: TFCModels,
        horizon: int,
        freq: str,
        add_holidays: bool = False,
        add_events: bool = False,
        country_isocode: str | None = None,
        future_variables: list[str] | None = None,
        historical_variables: list[str] | None = None,
        static_variables: list[str] | None = None,
        id_col: str = "unique_id",
        date_col: str = "ds",
        target_col: str = "target",
    ) -> pd.DataFrame:
        """Output crossvalidation predictions for a given model and train_df.

        Args:
            train_df (pd.DataFrame): Dataframe with historical target and features' values.
            fcds (list[dt.date  |  dt.datetime]):Forecast creation dates, ie, cutoff dates to dtermine the crossvalidation splits.
            model (TFCModels): Model to be used for forecasting.
            horizon (int): Number of steps to forecast.
            freq (str): Frequency Alias of the time series, e.g., H, D, W, M, Q, Y.
            add_holidays (bool, optional): Whether to include TFC-holidays as features. Defaults to False.
            add_events (bool, optional): Whether to include TFC-events as features. Defaults to False.
            country_isocode (str | None, optional): ISO (eg, US, GB,..) code of the country for which the forecast is requested. This is used for fetching the right
            holidays and events. Defaults to None.
            future_variables (list[str] | None, optional): Future variables to be used by the model. Defaults to None.
            historical_variables (list[str] | None, optional): Historical variables to be used by the model. Defaults to None.
            static_variables (list[str] | None, optional): Static variables to be used by the model. Defaults to None.
            id_col (str, optional): Column name in train_df and future_df containing the unique identifier of each time series. Defaults to "unique_id".
            date_col (str, optional): Column name in train_df and future_df containing the date of each time series. Defaults to "ds".
            target_col (str, optional): Column name in train_df containing the target of each time series. Defaults to "target".

        Returns:
            pd.DataFrame: Dataframe containing the crossvalidation predictions.
        """
        cvdf = cross_validate_single_model(
            train_df,
            fcds,
            model,
            horizon,
            freq,
            add_holidays,
            add_events,
            country_isocode,
            future_variables,
            historical_variables,
            static_variables,
            self.max_concurrent,
            self.max_tries,
            self.api_key,
            self.base_url,
            id_col,
            date_col,
            target_col,
        )
        # TODO: compute the cutoff dates automatically, to make sure they're all within the train_df.
        if cvdf[date_col].max() > train_df[date_col].max():
            raise ValueError("Forecast dates are outside the latest training date")
        cvdf = cvdf.merge(train_df[[id_col, date_col, target_col]], on=[id_col, date_col], how="left")
        if cvdf[target_col].isna().any():
            raise ValueError("Some target values are missing in the training data")
        return cvdf


class TFCAPIError(RuntimeError):
    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        response_body: Optional[str] = None,
    ):
        self.message = message
        self.status_code = status_code
        self.response_body = response_body
        super().__init__(self.message)

    def __str__(self):
        error_msg = f"{self.message}"
        if self.status_code:
            error_msg += f" (Status code: {self.status_code})"
        if self.response_body:
            error_msg += f"\nResponse body: {self.response_body}"
        return error_msg


class TFCBadRequestError(TFCAPIError):
    """Exception for 400 Bad Request errors."""

    pass


class TFCUnauthorizedError(TFCAPIError):
    """Exception for 401 Unauthorized errors."""

    pass


class TFCForbiddenError(TFCAPIError):
    """Exception for 403 Forbidden errors."""

    pass


class TFCNotFoundError(TFCAPIError):
    """Exception for 404 Not Found errors."""

    pass


class TFCUnprocessableEntityError(TFCAPIError):
    """Exception for 422 Unprocessable Entity errors."""

    pass


class TFCServerError(TFCAPIError):
    """Exception for 5xx Server errors."""

    pass
