declare var require: any

var React = require('react');
var ReactDOM = require('react-dom');

export class Hello extends React.Component {
    render() {
        return (
            <h1>Welcome to Weather App</h1>
        );
    }
}

ReactDOM.render(<Hello />, document.getElementById('root'));