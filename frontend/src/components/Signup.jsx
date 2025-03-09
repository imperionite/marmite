import React from "react";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { useForm } from "react-hook-form";
import { useNavigate, Link } from "react-router-dom";
import { toast } from "react-hot-toast";
import { sanitize } from "isomorphic-dompurify";
import * as yup from "yup";
import { yupResolver } from "@hookform/resolvers/yup";

import { signup } from "../services/http";
import { userKeys } from "../services/queryKeyFactory";

const Signup = () => {
  const queryClient = useQueryClient();
  const navigate = useNavigate();

  const mutate = useMutation({
    mutationFn: signup,
    onSuccess: (data) => {
      reset();
      toast.success(`${data?.message}`);
      queryClient.invalidateQueries({ queryKey: userKeys.all });
      queryClient.invalidateQueries({ queryKey: userKeys.lists() });
      queryClient.invalidateQueries({ queryKey: userKeys.details() });

      navigate("/login");
    },

    onError: (error) => {
      toast.error(`HTTP ${error.status}: ${error.code}`);
    },
  });

  const schema = yup
    .object({
      username: yup.string().trim().min(3).required(),
      email: yup.string().email().required(),
      password: yup.string().trim().min(7).required(),
      re_password: yup
        .string()
        .oneOf([yup.ref("password"), null], "Password must match"),
    })
    .required();

  const {
    register,
    reset,
    handleSubmit,
    getFieldState,
    formState: { errors },
  } = useForm({
    resolver: yupResolver(schema),
    mode: "all",
  });

  const onSubmit = async (input) => {
    const sanitizedData = {
      username: sanitize(input.username),
      email: sanitize(input.email),
      password: input.password,
    };
    const result = await mutate.mutateAsync(sanitizedData);

    return result;
  };

  const fieldStateUsername = getFieldState("username");
  const fieldStateEmail = getFieldState("email");
  const fieldStatePassword = getFieldState("password");
  const fieldStateRePassword = getFieldState("re_password");

  return (
    <>
      <h2>Signup for an account</h2>
      <form onSubmit={handleSubmit(onSubmit)} spellCheck="false" noValidate>
        <div className="grid">
          <label htmlFor="username">
            Username
            <input
              type="text"
              id="username"
              placeholder="Enter username"
              {...register("username")}
              aria-invalid={
                fieldStateUsername?.error !== undefined &&
                fieldStateUsername.isDirty
              }
              className={`${errors.username?.message ? "is-invalid" : ""} `}
              required
            />
            {errors.username && (
              <span className="error">{errors.username.message}</span>
            )}
          </label>

          <label htmlFor="email">
            Email
            <input
              type="email"
              id="email"
              placeholder="Enter email"
              {...register("email")}
              aria-invalid={
                fieldStateEmail?.error !== undefined && fieldStateEmail.isDirty
              }
              className={`${errors.email?.message ? "is-invalid" : ""} `}
              required
            />
            {errors.email && (
              <span className="error">{errors.email.message}</span>
            )}
          </label>
        </div>

        <div className="grid">
          <label htmlFor="password">
            Password
            <input
              type="password"
              id="password"
              placeholder="Enter password"
              {...register("password")}
              aria-invalid={
                fieldStatePassword.isDirty &&
                fieldStatePassword?.error !== undefined
              }
              className={`${errors.password?.message ? "is-invalid" : ""} `}
              required
            />
            {errors.password && (
              <span className="error">{errors.password.message}</span>
            )}
          </label>

          <label htmlFor="re_password">
            Password confirmation
            <input
              type="password"
              id="re_password"
              placeholder="Repeat password"
              {...register("re_password")}
              aria-invalid={
                fieldStateRePassword.isDirty &&
                fieldStateRePassword?.error !== undefined
              }
              className={`${errors.re_password?.message ? "is-invalid" : ""} `}
              required
            />
            {errors.re_password && (
              <span className="error">{errors.re_password.message}</span>
            )}
          </label>
        </div>

        <button aria-busy={mutate.isPending}>Submit</button>
      </form>

      <small>
        Already have an account? <Link to={"/login"}>Login to Connectly</Link>
      </small>
    </>
  );
};

export default Signup;
