import React, { useState, MouseEvent, useContext } from "react";
import { useNavigate } from "react-router-dom";
import Tabs from "@mui/material/Tabs";
import Tab from "@mui/material/Tab";
import useEmblaCarousel from "embla-carousel-react";
import TextField from "@mui/material/TextField";
import IconButton from "@mui/material/IconButton";
import Visibility from "@mui/icons-material/Visibility";
import VisibilityOff from "@mui/icons-material/VisibilityOff";
import OutlinedInput from "@mui/material/OutlinedInput";
import InputLabel from "@mui/material/InputLabel";
import InputAdornment from "@mui/material/InputAdornment";
import FormControl from "@mui/material/FormControl";
import Button from "@mui/material/Button";
import FormContainer from "../../general/FormContainer";
import {
  login,
  register,
  handleError,
  APIResponse,
  getCurrentUser,
} from "../../../services/api";
import { UserContext, UserData } from "../../../providers/UserProvider";
import { generateToast } from "../../../services/utils";
import "./index.css";

function LoginRegister() {
  const [tabIndex, setTabIndex] = useState(0);
  const [showPassword, setShowPassword] = useState(false);
  const { setUser } = useContext(UserContext);
  const navigate = useNavigate();

  const [emblaRef, emblaApi] = useEmblaCarousel({ loop: false });

  const tabChange = (event: React.SyntheticEvent, newIndex: number) => {
    setTabIndex(newIndex);
    if (emblaApi) {
      emblaApi.scrollTo(newIndex);
    }
  };

  const handleClickShowPassword = () => setShowPassword((show) => !show);

  const handleMouseDownPassword = (event: MouseEvent<HTMLButtonElement>) => {
    event.preventDefault();
  };

  const forms = new Map<string, string>([
    ["login", "Login"],
    ["register", "Register"],
  ]);

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    const target = e.target as HTMLFormElement & {
      username: HTMLInputElement;
      password: HTMLInputElement;
    };
    const formType = target.getAttribute("data-type");

    const submit = formType === "login" ? login : register;

    try {
      const res = await submit(target.username.value, target.password.value);
      const data = res.data as APIResponse;

      if (data.msg === "Logged in" || data.msg === "User created") {
        const userRes = await getCurrentUser();
        const userData = userRes.data as UserData;
        setUser(userData);

        navigate("/");

        generateToast(data.msg, "success");
      }
    } catch (e) {
      handleError(e);
    }
  };

  return (
    <FormContainer contentId="loginsignup-content">
      <Tabs value={tabIndex} onChange={tabChange} centered>
        {Array.from(forms).map(([id, label]) => (
          <Tab
            key={`loginsignup-tab-${id}`}
            className="loginsignup-tab"
            label={label}
          ></Tab>
        ))}
      </Tabs>
      <div className="embla" ref={emblaRef}>
        <div className="embla__container">
          {Array.from(forms).map(([id]) => (
            <form
              data-type={id}
              key={`loginsignup-${id}`}
              className="embla__slide loginsignup-form"
              onSubmit={handleSubmit}
            >
              <TextField
                name="username"
                className="loginsignup-form-textfield loginsignup-form-child"
                label="Username"
                variant="outlined"
                required
              />

              <FormControl
                className="loginsignup-form-textfield loginsignup-form-child"
                variant="outlined"
              >
                <InputLabel
                  htmlFor={`loginsignup-${id}-password-outlinedinput`}
                  required
                >
                  Password
                </InputLabel>
                <OutlinedInput
                  name="password"
                  type={showPassword ? "text" : "password"}
                  endAdornment={
                    <InputAdornment position="end">
                      <IconButton
                        className="loginsignup-form-show-pass"
                        onClick={handleClickShowPassword}
                        onMouseDown={handleMouseDownPassword}
                        edge="end"
                      >
                        {showPassword ? <VisibilityOff /> : <Visibility />}
                      </IconButton>
                    </InputAdornment>
                  }
                  label="Password"
                />
              </FormControl>
              <Button
                type="submit"
                variant="outlined"
                className="loginsignup-form-child loginsignup-form-submit"
              >
                Submit
              </Button>
            </form>
          ))}
        </div>
      </div>
    </FormContainer>
  );
}

export default LoginRegister;
