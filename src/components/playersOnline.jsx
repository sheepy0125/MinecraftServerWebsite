import {Component} from "react";
import {get} from "axios";

export default class PlayersOnline extends Component {
	state = {
		playersOnline: null,
		messageFlashed: null
	};

	// Get players online
	getPlayersOnline = () => {
		get("get_players_online_information")
			.then((result) => {
				if (result.data.worked) this.setState({playersOnline: result.data.player_informations, messageFlashed: null});
				else this.setState({messageFlashed: `Error: ${result.data.error_message}`});
			})
			.catch((result) => {
				this.setState({messageFlashed: "An error has occurred. " + JSON.stringify(result)});
			});
	};

	// Display players
	displayPlayers = () => {
		let playerDivs = [];
		for (const [username, information] of Object.entries(this.state.playersOnline)) {
			playerDivs.push(
				<div
					className="bg-gray-200 border-2 border-gray-300 mx-4 my-1 px-2 py-0 text-center rounded-lg 
					block sm:flex shadow-md transition duration-200 ease-in-out transform hover:scale-105"
					key={username}
				>
					<span className="py-2 block sm:flex-auto text-center sm:border-r border-gray-300">{username}</span>
					<span className="py-2 block sm:flex-auto text-center sm:border-l border-gray-300">{information.timeFormatted} played</span>
				</div>
			);
		}

		return playerDivs.length !== 0 ? (
			// Return the players if there are players online
			playerDivs
		) : (
			// But if there are no players online, then return a notice.
			<div className="bg-gray-200 border-2 border-gray-300 mx-4 my-1 p-2 text-center rounded-lg">No players are online.</div>
		);
	};

	componentDidMount = () => {
		this.getPlayersOnline();
	};

	render = () => {
		return (
			<div className="bg-opacity-50 hover:bg-opacity-75 bg-gray-50 border-2 border-gray-100 shadow-2xl text-center m-4 p-4 rounded-lg">
				<p className="font-semibold">Players online</p>
				<p>{this.state.messageFlashed}</p>
				{this.state.playersOnline !== null ? this.displayPlayers() : "No information."}
				<br />
				<button className="hover:bg-red-100 border-red-100 border-2" onClick={this.getPlayersOnline}>
					Refresh
				</button>
			</div>
		);
	};
}
