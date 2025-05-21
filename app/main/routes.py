from flask import session, redirect, url_for, render_template, request
from . import main
from .forms import LoginForm

@main.route('/web3/login', methods=['POST'])
def web3_login():
    data = request.json
    address = data.get('address')
    signature = data.get('signature')
    nonce = session.get('nonce')
    
    # Verify signature
    w3 = Web3()
    message = f"Login nonce: {nonce}"
    recovered_address = w3.eth.account.recover_message(
        text=message,
        signature=signature
    )
    
    if recovered_address.lower() == address.lower():
        session['name'] = address[:8]  # Use first 8 chars as username
        session['room'] = 'web3_chat'  # Default room for Web3 users
        return jsonify({'success': True})
    return jsonify({'error': 'Invalid signature'}), 401

@main.route('/web3/nonce')
def get_nonce():
    session['nonce'] = os.urandom(16).hex()
    return jsonify({'nonce': session['nonce']})

@main.route('/', methods=['GET', 'POST'])
def index():
    """Login form to enter a room."""
    form = LoginForm()
    if form.validate_on_submit():
        session['name'] = form.name.data
        session['room'] = form.room.data
        session['passw'] = form.passw.data  # Assuming you have a password field
        
        if session['passw'] == "!hj^ghvhHJdss7886#$#$Ihyg768L<L<spls":
            return redirect(url_for('.chat'))
        else:
            # Password is wrong - show error and stay on login page
            return render_template('index.html', form=form, error="Invalid password")
    
    # Handle GET request
    form.name.data = session.get('name', '')
    form.room.data = session.get('room', '')
    return render_template('index.html', form=form)


@main.route('/chat')
def chat():
    """Chat room. The user's name and room must be stored in the session."""
    name = session.get('name', '')
    room = session.get('room', '')
    passw = session.get('passw', '')
    
    if name == '' or room == '' or passw != "!hj^ghvhHJdss7886#$#$Ihyg768L<L<spls":
        return redirect(url_for('.index'))
    
    return render_template('chat.html', name=name, room=room)