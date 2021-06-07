import {Component} from "react";
import {get} from "axios";

export default class OtherLinks extends Component {
	state = {
		otherLinks: null
	};

	// Get links
	getLinks = () => {
		get("get_other_links")
			.then((linksResult) => {
				if (linksResult.data.worked) this.setState({otherLinks: linksResult.data.links});
				else this.setState({otherLinks: null});
			})
			.catch((result) => {
				this.setState({otherLinks: null});
			});
	};

	// Display links
	displayLinks = () => {
		let otherLinkItems = [];

		this.state.otherLinks.forEach((link) => {
			otherLinkItems.push(
				<li key={link.name} className="text-blue-500 hover:underline text-lg">
					<a href={link.url}>{link.name}</a>
				</li>
			);
		});

		return otherLinkItems;
	};

	componentDidMount = () => {
		this.getLinks();
	};

	render = () => {
		return (
			<div className="bg-opacity-50 hover:bg-opacity-75 bg-gray-50 p-4">
				<p className="font-semibold">Other links!</p>
				<ul className="mx-4 px-4">
					<div>{this.state.otherLinks !== null ? this.displayLinks() : "No information."}</div>
				</ul>
			</div>
		);
	};
}
