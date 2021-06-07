import {Component} from "react";
import {get} from "axios";

export default class ConnectionInstructions extends Component {
	state = {
		ipAddress: null,
		copyMessageFlashed: null,
		connectionInstructionsList: null
	};

	// Get connection instructions
	getConnectionInstructions = () => {
		get("get_connection_instructions")
			.then((instructionsResult) => {
				if (instructionsResult.data.worked)
					this.setState({connectionInstructionsList: instructionsResult.data.instructions, ipAddress: instructionsResult.data.ip_address});
				else this.setState({connectionInstructionsList: null, ipAddress: null});
			})
			.catch((result) => {
				this.setState({connectionInstructionsList: null, ipAddress: null});
			});
	};

	// Copy IP address
	copyIpAddress = () => {
		// Make sure IP address isn't null
		if (this.state.ipAddress === null) {
			this.setState({copyMessageFlashed: "Failed to get IP address to copy."});
			return;
		}

		navigator.clipboard.writeText(this.state.ipAddress);
		this.setState({copyMessageFlashed: "Copied to clipboard"});
	};

	// Display instructions
	displayInstructions = () => {
		let instructionsDivs = [];

		this.state.connectionInstructionsList.forEach((instruction) => {
			instructionsDivs.push(
				<div className="bg-gray-200 border-2 border-gray-300 m-1 p-2 text-center rounded-lg" key={instructionsDivs.length}>
					{instruction}
				</div>
			);
		});

		return instructionsDivs;
	};

	componentDidMount = () => {
		this.getConnectionInstructions();
	};

	render = () => {
		return (
			<div className="bg-opacity-50 hover:bg-opacity-75 bg-gray-50 p-4">
				<p className="font-semibold">How to connect</p>
				<div>{this.state.connectionInstructionsList !== null ? this.displayInstructions() : "No information."}</div>
				<button onClick={this.copyIpAddress}>Copy IP address</button>
				<p>{this.state.copyMessageFlashed}</p>
			</div>
		);
	};
}
