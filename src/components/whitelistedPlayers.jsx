import {Component} from "react";
import {get} from "axios";

export default class WhitelistedPlayers extends Component {
	state = {
		whitelistedPlayers: null,
		messageFlashed: null
	};

	// Get players
	getPlayers = () => {
		get("get_whitelisted_players")
			.then((result) => {
				if (result.data.worked) this.setState({whitelistedPlayers: result.data.players, messageFlashed: null});
				else this.setState({messageFlashed: `Error: ${result.data.error_message}`});
			})
			.catch((result) => {
				this.setState({messageFlashed: "An error has occurred. " + JSON.stringify(result)});
			});
	};

	// Display players
	displayPlayers = () => {
		let whitelistedPlayersDivs = [];

		this.state.whitelistedPlayers.forEach((player) => {
			whitelistedPlayersDivs.push(
				<div
					className="bg-gray-200 border-2 border-gray-300 m-1 p-2 text-center rounded-lg  
								shadow-md transition duration-200 ease-in-out transform hover:scale-105"
					key={player}
				>
					{player}
				</div>
			);
		});

		return whitelistedPlayersDivs;
	};

	componentDidMount = () => {
		this.getPlayers();
	};

	render = () => {
		return (
			<div className="bg-opacity-50 hover:bg-opacity-75 bg-gray-50 border-2 border-gray-100 shadow-2xl text-center m-4 p-4 rounded-lg row-span-2">
				<p className="font-semibold">Whitelisted players</p>
				<p>{this.state.messageFlashed}</p>
				{this.state.whitelistedPlayers !== null ? (
					<div className="block sm:grid sm:grid-cols-2 xl:grid-cols-3">{this.displayPlayers()}</div>
				) : (
					<p className="">No information.</p>
				)}
				<br />
			</div>
		);
	};
}
