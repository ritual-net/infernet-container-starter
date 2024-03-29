import { ButtonHTMLAttributes, PropsWithChildren } from "react";

export const Button = (
  p: PropsWithChildren<ButtonHTMLAttributes<HTMLButtonElement>>,
) => (
  <button
    className={"bg-emerald-700 font-light px-4 py-2 rounded-xl text-white"}
    {...p}
  />
);
