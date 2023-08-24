import { PropsWithChildren } from "react";
import "./index.css";

interface FormContainerProps {
  id?: string;
  contentId?: string;
}

function FormContainer({
  children,
  id,
  contentId,
}: FormContainerProps & PropsWithChildren) {
  return (
    <div id={id} className="formcontainer">
      <div id={contentId} className="formcontainer-content">
        {children}
      </div>
    </div>
  );
}

export default FormContainer;
