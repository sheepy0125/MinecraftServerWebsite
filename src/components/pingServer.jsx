import {Component, Fragment} from "react";
import {get} from "axios";

export default class PingServer extends Component {
	state = {
		ping: null
	};

	componentDidMount = () => {
		// Get ping once every 5 seconds
		this.getPing();
		this.pingLoop = setInterval(this.getPing, 5000);
	};

	componentWillUnmount = () => {
		// Remove the ping loop
		clearInterval(this.pingLoop);
	};

	// Get ping
	getPing = () => {
		const startPingTime = Date.now() / 1000;
		get("/ping")
			.then((result) => {
				const endPingTime = Date.now() / 1000;
				this.setState({ping: endPingTime - startPingTime});
			})
			.catch((result) => {
				this.setState({ping: null});
			});
	};

	render = () => {
		return (
			<Fragment>
				<div className={"bg-" + (this.state.ping !== null ? "white" : "red-500") + " mx-auto block w-max"}>
					{this.state.ping !== null
						? `You're connected to the server! Your ping is ${Math.round(this.state.ping * 1000) / 1000} ms.`
						: "You're not connected to the server."}
				</div>
			</Fragment>
		);
	};
}
