import { useCallback, useEffect, useState } from "react";
import { Quiz } from "../api/@types";

type AsyncState = {
  data?: Quiz[] | undefined;
  loading: boolean;
  error?: Error | undefined;
};

const initialState: AsyncState = {data: undefined, loading: false, error: undefined}

export const useAsync = <T extends Quiz[] | undefined>(asyncFn: () => Promise<T>)=> {
  const [state, setState] = useState<AsyncState>(initialState);

  useEffect(() => {
    setState((prev) => ({ ...prev, loading: true }));
      asyncFn().then(
        (res) => {
          setState((prev) => ({ ...prev, data: res, loading: false }));
        },
        (err) => {
          setState((prev) => ({ ...prev, error: err, loading: false }));
        }
    );
  }, []);
  return state;
}

/*export const useAsync = (asyncFn: any, immediate = false) => {
  // four status to choose ["idle", "pending", "success", "error"]
  const [state, setState] = useState({
    status: "idle",
    value: null,
    error: null,
  });

  // return the memoized function
  // useCallback ensures the below useEffect is not called
  // on every render, but only if asyncFunction changes.
  const refetch = useCallback(() => {
    // reset the state before call
    setState({
      status: "pending",
      value: null,
      error: null,
    });

    return asyncFn()
      .then((response: any) => {
        setState({
          status: "success",
          value: response,
          error: null,
        });
      })
      .catch((error: any) => {
        setState({
          status: "error",
          value: null,
          error: error,
        });
      });
  }, [asyncFn]);

  // execute the function
  // if asked for immediate
  useEffect(() => {
    if (immediate) {
      refetch();
    }
  }, [refetch, immediate]);

  // state values
  const { status, value, error } = state;

  return { refetch, status, value, error };
};*/