import MenuItem from "@mui/material/MenuItem";
import Select from "@mui/material/Select";
import AddCircleOutlineIcon from "@mui/icons-material/AddCircleOutline";
import { useNavigate } from "react-router-dom";
import "./index.css";

function CreateDropdown() {
  const navigate = useNavigate();

  return (
    <Select
      className="createdropdown"
      IconComponent={AddCircleOutlineIcon}
      variant="standard"
      MenuProps={{ PaperProps: { className: "createdropdown-paper" } }}
    >
      <MenuItem onClick={(e) => navigate("/submit/subforum")}>
        Create Subforum
      </MenuItem>
      <MenuItem onClick={(e) => navigate("/submit/post")}>Create Post</MenuItem>
    </Select>
  );
}

export default CreateDropdown;
