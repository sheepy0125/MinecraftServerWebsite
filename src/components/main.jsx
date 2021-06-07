// Main page

import React, {Component} from "react";
import ConnectionInstructions from "./connectionInstructions.jsx";
import Rules from "./rules.jsx";
import ServerStatus from "./serverStatus.jsx";
import PlayersOnline from "./playersOnline.jsx";
import WhitelistedPlayers from "./whitelistedPlayers.jsx";
import Contact from "./contact.jsx";
import OtherLinks from "./otherLinks.jsx";

export default class Main extends Component {
	render = () => {
		return (
			<React.Fragment>
				{/* No CSS */} <h2 className="hidden">It seems you do not have CSS enabled. Please note that the website won't look good without CSS.</h2>
				<div className="max-w-max mx-auto">
					<div className="bg-opacity-50 bg-white p-4 rounded-lg text-5xl text-center font-semibold m-4">Minecraft Server Website</div>
					<div className="bg-opacity-50 bg-white text-center rounded-lg m-4 p-4">
						<p className="text-xl font-semibold">Information</p>

						<div className="block md:grid grid-flow-col md:grid-cols-2 md:grid-rows-2">
							<ServerStatus />
							<PlayersOnline />
							<WhitelistedPlayers />
						</div>

						<div className="border-2 border-gray-100 shadow-2xl text-center m-4 rounded-lg">
							<Rules />
							<ConnectionInstructions />
							<OtherLinks />
						</div>

						<Contact />
					</div>
				</div>
			</React.Fragment>
		);
	};
}
