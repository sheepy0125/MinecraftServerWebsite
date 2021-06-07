import {Component} from "react";
import {get} from "axios";

export default class ServerStatus extends Component {
	state = {
		serverStatusInformation: null,
		messageFlashed: null
	};

	// Get status
	getStatus = () => {
		get("get_server_status")
			.then((result) => {
				if (result.data.worked) this.setState({serverStatusInformation: result.data.information, messageFlashed: null});
				else this.setState({messageFlashed: `Error: ${result.data.error_message}`});
			})
			.catch((result) => {
				this.setState({messageFlashed: "An error has occurred. " + JSON.stringify(result)});
			});
	};

	// Display status
	displayStatus = () => {
		const information = this.state.serverStatusInformation;
		return (
			<div className="bg-gray-200 border-2 border-gray-300 mx-4 my-1 p-2 text-center rounded-lg">
				{information.serverUp ? "The server is currently up." : "The server is currently down (!!!)"}
				<p>
					The server has been {information.serverUp ? "up" : "down"} for {information.timeFormatted}.
				</p>
			</div>
		);
	};

	componentDidMount = () => {
		this.getStatus();
		this.realtimeUpdate = setInterval(this.getStatus, 5000);
	};

	componentWillUnmount = () => {
		clearInterval(this.realtimeUpdate);
	};

	render = () => {
		return (
			<div className="bg-opacity-50 hover:bg-opacity-75 bg-gray-50 border-2 border-gray-100 shadow-2xl text-center m-4 p-4 rounded-lg">
				<p className="font-semibold">Server status</p>
				<p>{this.state.messageFlashed}</p>
				{this.state.serverStatusInformation !== null ? this.displayStatus() : "No information."}
				<p>This updates once every 5 seconds.</p>
			</div>
		);
	};
}
