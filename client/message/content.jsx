const React = require('react'),
      Text = require('./text.jsx'),
      Image = require('./image.jsx');

class MessageContent extends React.Component {
    render() {
        var message_content = this.props.message_content;
        var messageType = this.props.messageType;
        var message_class = null;

        switch (messageType) {
            case 'text':
                message_class = <Text message_content={message_content} />;
            break;

            case 'image':
                message_class = <Image message_content={message_content} />;
            break;
        }

        return message_class;
    }
}

module.exports = MessageContent;
