import React from 'react';
import {Launcher} from 'react-chat-window'
import { async } from 'q';

class Chatwindow extends React.Component {

  constructor() {
    super();
    this.state = {
      messageList: [],
      // newMessagesCount: 0,
      status: "initial"
    };
    this._sendMessage = this._sendMessage.bind(this);
  }
  
  componentDidMount() {
    fetch("http://localhost:5000")
    .then(res => res.json())
    .then((result) => this._sendMessage(result.msg))
  }

  async _onMessageWasSent(message) {
    this.setState({
      messageList: [...this.state.messageList, message]
    });
    const rawResponse = await fetch('http://localhost:5000/messagehandler', {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({msg: message})
    });
    const content = await rawResponse.json();
    console.log(content);
    this._sendMessage(content.msg)
  }

  _sendMessage(text) {
    if (text.length > 0) {
      this.setState({
        messageList: [...this.state.messageList, {
          author: 'them',
          type: 'text',
          data: { text }
        }]
      })
    }
  }

  render() {
    return (
      <div>
        <Launcher
          agentProfile={{
            teamName: 'Payments team',
            imageUrl: 'https://a.slack-edge.com/66f9/img/avatars-teams/ava_0001-34.png'
          }}
          onMessageWasSent={this._onMessageWasSent.bind(this)}
          messageList={this.state.messageList}
          showEmoji
        />
      </div>
    )
  }
}

export default Chatwindow;
