import {Component} from "react";
import {post} from "axios";

export default class ServerStatus extends Component {
	state = {
		charsLeftMessage: 1800
	};

	// Submit confirm
	submitResponseConfirm = () => {
		// Make sure response can be submitted
		const usernameContent = document.getElementById("username-input").value;
		const messageContent = document.getElementById("message-input").value;

		if (usernameContent.length === 0 || messageContent.length === 0) {
			alert("Your username and message must not be empty.");
			return;
		}

		if (window.confirm("Are you sure that you want to send this message to Pink_Sheepy?")) this.submitResponse(usernameContent, messageContent);
	};

	// Submit response
	submitResponse = (usernameContent, messageContent) => {
		post(
			"/contact_sheepy",
			{
				username: usernameContent,
				message: messageContent
			},
			{
				headers: {
					"Content-Type": "application/json"
				}
			}
		)
			.then((result) => {
				if (result.data.worked) alert("Success! Your message has been sent to Pink_Sheepy.");
				else alert("Your message was rejected! The server sent this response: " + JSON.stringify(result.data));
			})
			.catch((result) => {
				alert("Ah crap it didn't work... Give this information to sheepy (wish you could use the contact sheepy now huh) " + JSON.stringify(result));
			});
	};

	// Handle message keystroke
	handleMessageKeystroke = (event) => {
		this.setState({charsLeftMessage: 1800 - event.target.value.length});
	};

	render = () => {
		this.renders++;
		return (
			<div className="bg-opacity-50 hover:bg-opacity-75 bg-gray-50 border-2 border-gray-100 shadow-2xl text-center m-4 p-4 rounded-lg">
				<p className="font-semibold">Contact Pink_Sheepy</p>
				<label>
					Discord username
					<br />
					<input type="text" className="w-3/4" id="username-input" maxLength="32" />
					<br />
					Message ({this.state.charsLeftMessage} characters left)
					<br />
					<textarea className="h-20 w-3/4" id="message-input" maxLength="1800" onChange={this.handleMessageKeystroke} />
					<br />
				</label>
				<button type="submit" className="p-4 m-2 bg-green-400 hover:bg-green-500 rounded-lg w-1/3" onClick={this.submitResponseConfirm}>
					Send
				</button>
				<p className="text-sm">
					This will ping Pink_Sheepy on Discord. Please note that you may only do this once every 3 minutes and may not edit or delete the message.
				</p>
			</div>
		);
	};
}
