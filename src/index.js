import ReactDOM from "react-dom";
import "./index.css";

import PingServer from "./components/pingServer";
import Main from "./components/main";

// Render
ReactDOM.render(<Main />, document.getElementById("root"));
ReactDOM.render(<PingServer />, document.getElementById("ping-result"));
