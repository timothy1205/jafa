import { useNavigate } from "react-router-dom";
import { APIResponse, createPost, handleError } from "../../../services/api";
import JafaForm, {
  JafaFormContainer,
  JafaButton,
  JafaTextField,
  JafaHeader,
} from "../../general/JafaForm";
import "./index.css";
import { generateToast } from "../../../services/utils";

function PostCreateForm() {
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    const target = e.target as HTMLFormElement & {
      subforum: HTMLInputElement;
      title: HTMLInputElement;
      body: HTMLTextAreaElement;
    };

    try {
      const res = await createPost(
        target.subforum.value,
        target.title.value,
        target.body.value
      );
      const data = res.data as APIResponse;

      if (data.msg === "Post created") {
        navigate(`/subforum/${target.subforum.value}`);
        generateToast(data.msg, "success");
      } else {
        throw Error(`Unknown response: ${data.msg}`);
      }
    } catch (e) {
      handleError(e);
    }
  };

  return (
    <JafaFormContainer contentId="postcreate-content">
      <JafaForm onSubmit={handleSubmit}>
        <JafaHeader>Create Post</JafaHeader>
        <JafaTextField
          name="subforum"
          className="postcreate-child"
          label="Subforum"
          required
        />
        <JafaTextField
          name="title"
          className="postcreate-child"
          label="Title"
          required
        />
        <JafaTextField
          name="body"
          className="postcreate-child"
          label="Body"
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

export default PostCreateForm;
