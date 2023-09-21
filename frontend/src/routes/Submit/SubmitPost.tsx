import PostCreateForm from "../../components/submit/PostCreateForm";
import ProtectedRoute from "../ProtectedRoute";

function SubmitPost() {
  return (
    <ProtectedRoute>
      <PostCreateForm />
    </ProtectedRoute>
  );
}

export default SubmitPost;
