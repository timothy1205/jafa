import { PropsWithChildren } from "react";
import TextField from "@mui/material/TextField";
import FormControl from "@mui/material/FormControl";
import Button from "@mui/material/Button";
import "./index.css";

export default function JafaForm(props: React.ComponentProps<"form">) {
  const className = `jafa-form ${props.className ?? ""}`;

  return (
    <form {...props} className={className}>
      {props.children}
    </form>
  );
}

interface FormContainerProps {
  id?: string;
  contentId?: string;
}

export function JafaFormContainer({
  children,
  id,
  contentId,
}: FormContainerProps & PropsWithChildren) {
  return (
    <div id={id} className="jafa-formcontainer">
      <div id={contentId} className="formcontainer-content">
        {children}
      </div>
    </div>
  );
}

type JafaTextFieldProps = Omit<Parameters<typeof TextField>[0], "variant">;

export function JafaTextField(props: JafaTextFieldProps) {
  const className = `${props.className ?? ""} jafa-formtextfield`;

  return <TextField {...props} className={className} variant="outlined" />;
}

type JafaFormControlProps = Omit<Parameters<typeof FormControl>[0], "variant">;

export function JafaFormControl(props: JafaFormControlProps) {
  const className = `jafa-formtextfield ${props.className ?? ""}`;

  return (
    <FormControl {...props} className={className} variant="outlined">
      {props.children}
    </FormControl>
  );
}

type JafaButtonProps = Omit<Parameters<typeof Button>[0], "variant">;

export function JafaButton(props: JafaButtonProps) {
  const className = `jafa-formbutton ${props.className ?? ""}`;

  return (
    <Button {...props} className={className} variant="outlined">
      {props.children}
    </Button>
  );
}

export function JafaHeader(props: React.ComponentProps<"h1">) {
  const className = `jafa-formheader ${props.className ?? ""}`;
  return (
    <h1 {...props} className={className}>
      {props.children}
    </h1>
  );
}
