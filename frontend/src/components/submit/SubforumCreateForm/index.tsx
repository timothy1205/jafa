import { useNavigate } from "react-router-dom";
import {
  APIResponse,
  createSubforum,
  handleError,
} from "../../../services/api";
import JafaForm, {
  JafaFormContainer,
  JafaButton,
  JafaTextField,
  JafaHeader,
} from "../../general/JafaForm";
import "./index.css";
import { generateToast } from "../../../services/utils";

function SubforumCreateForm() {
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    const target = e.target as HTMLFormElement & {
      title: HTMLInputElement;
      description: HTMLTextAreaElement;
    };

    try {
      const res = await createSubforum(
        target.title.value,
        target.description.value
      );
      const data = res.data as APIResponse;

      if (data.msg === "Subforum created") {
        navigate(`/subforum/${target.title.value}`);
        generateToast(data.msg, "success");
      } else {
        throw Error(`Unknown response: ${data.msg}`);
      }
    } catch (e) {
      handleError(e);
    }
  };

  return (
    <JafaFormContainer contentId="subforumcreate-content">
      <JafaForm onSubmit={handleSubmit}>
        <JafaHeader>Create Subforum</JafaHeader>
        <JafaTextField
          name="title"
          className="subforumcreate-child"
          label="Title"
          required
        />
        <JafaTextField
          name="description"
          className="subforumcreate-child"
          label="Description"
          required
          multiline
        />

        <JafaButton type="submit" className="">
          Create
        </JafaButton>
      </JafaForm>
    </JafaFormContainer>
  );
}

export default SubforumCreateForm;
