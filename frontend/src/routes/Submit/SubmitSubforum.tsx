import SubforumCreateForm from "../../components/submit/SubforumCreateForm";
import ProtectedRoute from "../ProtectedRoute";

function SubmitSubforum() {
  return (
    <ProtectedRoute>
      <SubforumCreateForm />
    </ProtectedRoute>
  );
}

export default SubmitSubforum;
