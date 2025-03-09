import React from "react";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { useSetAtom } from "jotai";
import { useForm } from "react-hook-form";
import { yupResolver } from "@hookform/resolvers/yup";
import { useNavigate, Link } from "react-router-dom";
import { toast } from "react-hot-toast";
import { sanitize } from "isomorphic-dompurify";
import { jwtDecode } from "jwt-decode";
import * as yup from "yup";
import { useGoogleLogin } from '@react-oauth/google';

import { login, googleLogin } from "../services/http";
import { userKeys, postKeys } from "../services/queryKeyFactory";
import { jwtAtom, expAtom } from "../atoms/store";

const Login = () => {
  const queryClient = useQueryClient();
  const navigate = useNavigate();
  const setJwt = useSetAtom(jwtAtom);
  const setExp = useSetAtom(expAtom);
  //const googleClientId = import.meta.env.VITE_GOOGLE_CLIENT_ID;

  const schema = yup
    .object({
      identifier: yup
        .string()
        .required("Enter your registered email or username"),
      password: yup.string().required(),
    })
    .required();

  const mutation = useMutation({
    mutationFn: login,
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: userKeys.lists() });
      queryClient.invalidateQueries({ queryKey: userKeys.details() });
      queryClient.invalidateQueries({ queryKey: postKeys.list() });
      queryClient.invalidateQueries({ queryKey: postKeys.details() });

      const decoded = jwtDecode(data.access);
      setJwt({ access: data?.access, refresh: data?.refresh });
      toast.success(`Hi user ${decoded?.user_id}`);
      reset();
      navigate("/dashboard");
      if (typeof decoded.exp === "number") setExp(decoded.exp);
    },
    onError: (error) => {
      toast.error(`HTTP ${error.status}: ${error.code}`);
    },
  });


  const googleLoginMutation = useMutation({
    mutationFn: googleLogin,
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: userKeys.lists() });
      queryClient.invalidateQueries({ queryKey: userKeys.details() });
      queryClient.invalidateQueries({ queryKey: postKeys.list() });
      queryClient.invalidateQueries({ queryKey: postKeys.details() });

      const decoded = jwtDecode(data.access);
      setJwt({ access: data?.access, refresh: data?.refresh });
      toast.success(`Hi user ${decoded?.user_id}`);
      navigate('/dashboard');
      if (typeof decoded.exp === 'number') setExp(decoded.exp);
    },
    onError: (error) => {
      toast.error('Login failed:', error);
    },
  });

  const handleGoogleSuccess = (response) => {
    googleLoginMutation.mutate(response.access_token);
  };

  const handleGoogleFailure = (response) => {
    toast.error('Google login failed:', response);
  };

  const gLogin = useGoogleLogin({
    onSuccess: handleGoogleSuccess,
    onError: handleGoogleFailure,
    redirect_uri: 'http://localhost:8000/accounts/google/login/callback/'
  });

  const {
    register,
    reset,
    handleSubmit,
    getFieldState,
    formState: { errors },
  } = useForm({
    resolver: yupResolver(schema),
    mode: "all",
    defaultValues: {
      identifier: "",
      password: "",
    },
  });

  const onSubmit = (input) => {
    const sanitizedData = {
      identifier: sanitize(input.identifier),
      password: input.password,
    };
    mutation.mutate(sanitizedData);
  };

  const fieldStateIdentifier = getFieldState("identifier");
  const fieldStatePassword = getFieldState("password");

  return (
    <div style={{ maxWidth: "400px", margin: "auto", padding: "20px" }}>
      <h2>Login</h2>
      <form onSubmit={handleSubmit(onSubmit)} spellCheck="false" noValidate>
        <div>
          <label htmlFor="identifier">
            Email or Username
            <input
              type="text"
              id="identifier"
              placeholder="Enter your username or email"
              {...register("identifier", { required: true })}
              aria-invalid={
                fieldStateIdentifier.invalid && fieldStateIdentifier.isDirty
              }
              style={{
                border: fieldStateIdentifier.invalid
                  ? "2px solid red"
                  : fieldStateIdentifier.isDirty &&
                    !fieldStateIdentifier.invalid
                  ? "2px solid green"
                  : "1px solid #ccc",
                padding: "8px",
                borderRadius: "4px",
                width: "100%",
              }}
            />
            {errors.identifier && (
              <small style={{ color: "red", display: "block" }}>
                {errors.identifier.message}
              </small>
            )}
          </label>

          <label htmlFor="password" style={{ marginTop: "1rem" }}>
            Password
            <input
              type="password"
              id="password"
              placeholder="Enter password"
              {...register("password", { required: true })}
              aria-invalid={
                fieldStatePassword.isDirty && fieldStatePassword.invalid
              }
              style={{
                border: fieldStatePassword.invalid
                  ? "2px solid red"
                  : fieldStatePassword.isDirty && !fieldStatePassword.invalid
                  ? "2px solid green"
                  : "1px solid #ccc",
                padding: "8px",
                borderRadius: "4px",
                width: "100%",
              }}
            />
            {errors.password && (
              <small style={{ color: "red", display: "block" }}>
                {errors.password.message}
              </small>
            )}
          </label>
        </div>

        <button type="submit" disabled={mutation.isPending}>
          {mutation.isPending ? "Submitting..." : "Submit"}
        </button>
      </form>
      <hr />

      <div>
      <button onClick={() => gLogin()}>Sign in with Google</button>
      </div>
      <hr />

      <small style={{ display: "block", marginTop: "10px" }}>
        Need an account? <Link to={"/signup"}>Signup to Connectly</Link>
      </small>
    </div>
  );
};

export default Login;
