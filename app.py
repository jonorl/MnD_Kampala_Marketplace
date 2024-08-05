import os
import logging
import uuid
import re

from datetime import datetime
from flask import Flask, flash, redirect, render_template, jsonify, url_for, send_from_directory, request, session, current_app
from flask_login import LoginManager, UserMixin, login_required,  current_user
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from PIL import Image
from sqlalchemy.orm import joinedload
from sqlalchemy import or_, func
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, usd, ugx

# Configure application
app = Flask(__name__)

def is_mobile(user_agent_string):
    """Check if user agent is a mobile device"""
    mobile_patterns = [
        'Mobile', 'Android', 'iPhone', 'iPad', 'Windows Phone',
        'BlackBerry', 'Nokia', 'Opera Mini', 'webOS'
    ]
    return any(pattern in user_agent_string for pattern in mobile_patterns)

# Set up the upload folder
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['UPLOAD_FOLDER'] = os.path.join(basedir, 'static', 'uploads')

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Set maximum file size to 500 KB
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10 MB in bytes

# Configure database
app.config['STATIC_URL_PATH'] = '/static'
app.config['STATIC_FOLDER'] = '/home/jonorl/mysite/static'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movingsale.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Custom filters
app.jinja_env.filters["usd"] = usd
app.jinja_env.filters["ugx"] = ugx

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# Define models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    hash = db.Column(db.String(255), nullable=False)

    items = db.relationship('Item', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(100))
    location = db.Column(db.String(20))

    items = db.relationship('Item', backref='contact', lazy=True)

    def __repr__(self):
        return f'<Contact {self.name}>'

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    contact_id = db.Column(db.Integer, db.ForeignKey('contact.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String)
    price = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(3), nullable=False)
    availability = db.Column(db.String(50))
    image_path = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    sold = db.Column(db.Boolean, default=False)
    thumbnail_path = db.Column(db.String(255))

    def __repr__(self):
        return f'<Item {self.name}>'

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
def index():
    """Show paginated list of items"""
    page = request.args.get('page', 1, type=int)
    per_page = 10  # Number of items per page
    search = request.args.get('search', '')
    date = request.args.get('date')  # Get the date from the request
    username = request.args.get('username')  # Get the username from the request
    exclude_sold = request.args.get('exclude_sold')  # Get the exclude sold checkbox value

    # Retrieve all users for the dropdown
    users = User.query.all()

    # Base query
    query = Item.query

    # Apply search if a search term is provided
    if search:
        query = query.filter(or_(
            Item.name.ilike(f'%{search}%'),
            Item.description.ilike(f'%{search}%'),
            Item.contact.has(name=search),
            Item.contact.has(location=search)
        ))

    # Apply date filter if a date is provided
    if date:
        query = query.filter(func.date(Item.created_at) == date)

    # Apply user filter if a username is provided
    if username:
        query = query.filter(Item.user_id == username)

    # Apply exclude sold filter if the checkbox is checked
    if exclude_sold:
        query = query.filter(Item.sold == 0)

    # Use paginate instead of all()
    items = query.order_by(Item.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)


    user_agent = request.headers.get('User-Agent')
    is_mobile_device = is_mobile(user_agent)

    return render_template("index_mobile.html" if is_mobile_device else "index.html", items=items, search=search, date=date, users=users, str=str, exclude_sold=exclude_sold, is_mobile=is_mobile_device)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Query database for username
        user = User.query.filter_by(username=request.form.get("username")).first()

        # Ensure username exists and password is correct
        if user is None or not check_password_hash(user.hash, request.form.get("password")):
            return apology("invalid username and/or password", 400)

        # Remember which user has logged in
        session["user_id"] = user.id

        # Redirect user to home page
        flash("Logged in successfully!")
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    flash("Logged out successfully!")
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Validate input
        if not username:
            return apology("must provide username", 400)
        elif not password:
            return apology("must provide password", 400)
        elif password != confirmation:
            return apology("passwords must match", 400)

        # Check if username already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return apology("username already taken", 400)

        # Create new user
        new_user = User(username=username, hash=generate_password_hash(password))
        db.session.add(new_user)
        db.session.commit()

        flash("Registered successfully!")
        return redirect("/login")
    else:
        return render_template("register.html")

@app.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    """Change user's password"""
    if request.method == "POST":
        current_password = request.form.get("currentpassword")
        new_password = request.form.get("newpassword")
        confirmation = request.form.get("confirmation")

        # Validate input
        if not current_password:
            return apology("must provide current password", 400)
        elif not new_password:
            return apology("must provide new password", 400)
        elif new_password != confirmation:
            return apology("new passwords must match", 400)

        # Check current password
        user = User.query.get(session["user_id"])
        if not check_password_hash(user.hash, current_password):
            return apology("current password is incorrect", 400)

        # Update password
        user.hash = generate_password_hash(new_password)
        db.session.commit()

        flash("Password changed successfully!")
        return redirect("/logout")
    else:
        return render_template("change_password.html")

@app.route("/list_new_items", methods=['GET', 'POST'])
@login_required
def list_new_items():
    if request.method == 'POST':
        # Process form data
        contact_name = request.form.get('name')
        phone = request.form.get('phone')
        email = request.form.get('email')
        location = request.form.get('location')

        # Create new contact
        new_contact = Contact(name=contact_name, phone=phone, email=email, location=location)
        db.session.add(new_contact)
        db.session.flush()  # Get new_contact.id before commit

        # Add items
        index = 0
        while True:
            name = request.form.get(f'items[{index}][name]')
            if not name:
                break  # Stop if no more items are present

            description = request.form.get(f'items[{index}][description]')
            price = request.form.get(f'items[{index}][price]')
            currency = request.form.get(f'items[{index}][currency]')
            availability = request.form.get(f'items[{index}][availability]')

            # Handle image upload
            image_file = request.files.get(f'items[{index}][image]')

            # Ensure the required fields are present
            if not name or not price or not currency:
                index += 1
                continue  # Skip this item if mandatory fields are missing

            try:
                # Convert price to float and create new Item
                new_item = Item(
                    user_id=session.get("user_id"),
                    contact_id=new_contact.id,
                    name=name,
                    description=description,
                    price=float(price),
                    currency=currency,
                    availability=availability
                )
                db.session.add(new_item)
                db.session.flush()  # This gives new_item an ID

                # Process and store image if provided
                if image_file:
                    original_path, thumbnail_path = handle_image_upload(image_file, new_item.id)
                    if original_path and thumbnail_path:
                        store_image_paths(new_item.id, original_path, thumbnail_path)
                    else:
                        current_app.logger.warning(f"Failed to process image for item {new_item.id}")

            except ValueError:
                flash(f"Invalid price for item {name}. Please enter a valid number.", "error")
            except Exception as e:
                current_app.logger.error(f"Error processing item {name}: {str(e)}")
                flash(f"An error occurred while processing item {name}. Please try again.", "error")

            index += 1

        try:
            db.session.commit()
            flash('Items listed successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error committing to database: {str(e)}")
            flash('An error occurred while saving your items. Please try again.', 'error')

        return redirect(url_for('index'))

    # GET request
    items = [{'name': '', 'description': '', 'price': '', 'currency': 'UGX', 'availability': ''}]
    return render_template('list_new_items.html', items=items)


@app.route('/modify_listing', methods=['GET', 'POST'])
@login_required
def modify_listing():
    if "user_id" in session:
        logging.info(f"user_id is set: {session['user_id']}")
    else:
        logging.error("user_id is not set in session")
    if request.method == 'POST':
        for item in Item.query.filter_by(user_id=session["user_id"]).all():

            name = request.form.get(f'name-{item.id}')
            description = request.form.get(f'description-{item.id}')
            price = request.form.get(f'price-{item.id}')
            currency = request.form.get(f'currency-{item.id}')
            sold = 'sold-{}'.format(item.id) in request.form

            # Update item attributes
            item.name = name
            item.description = description
            item.price = price
            item.currency = currency
            item.sold = sold

            # Get new image and remove image request
            image_file = request.files.get(f'image-{item.id}')
            remove_image = request.form.get(f'remove-image-{item.id}') == 'on'


            #these lines of code fix the prefix issue when running the server from Codespaces/VSCode

            prefix = '/workspaces/39122230/final_project'
            old_image_path = item.image_path
            old_thumbnail_path = item.thumbnail_path

            if item.image_path and not item.image_path.startswith(prefix):
                old_image_path = prefix + item.image_path

            if item.thumbnail_path and not item.thumbnail_path.startswith(prefix):
                old_thumbnail_path = prefix + item.thumbnail_path


            if remove_image:
                # Remove the current image from the filesystem and database
                if old_image_path:
                    try:
                        os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'], old_image_path))
                        os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'], old_thumbnail_path))
                    except FileNotFoundError:
                        pass  # Ignore if the file does not exist

                item.image_path = None
                item.thumbnail_path = None

            elif image_file and allowed_file(image_file.filename):
                # Remove the old image if a new one is uploaded
                if old_image_path:
                    try:
                        os.remove(old_image_path)
                        os.remove(old_thumbnail_path)
                        #print("UPLOAD_FOLDER:", current_app.config['UPLOAD_FOLDER'])
                        #print("Old Image Path:", old_image_path)
                        #print("Old Thumbnail Path:", old_thumbnail_path)
                        #os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'], old_image_path))
                        #os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'], old_thumbnail_path))
                    except FileNotFoundError:
                        pass  # Ignore if the file does not exist

                # Upload and save the new image
                original_path, thumbnail_path = handle_image_upload(image_file, item.id)
                if original_path and thumbnail_path:
                    store_image_paths(item.id, original_path, thumbnail_path)

        db.session.commit()
        return jsonify(success=True)

    items = Item.query.filter_by(user_id=session["user_id"]).all()
    return render_template('modify_listing.html', items=items)


@app.route('/delete_item/<int:item_id>', methods=['POST'])
def delete_item(item_id):
    item = Item.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return jsonify(success=True)


@app.template_filter('currency')
def currency_filter(value):
    return f"{value:,.2f}"



# Add more routes for item management (add, edit, delete) here

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

def handle_image_upload(image_file, item_id):
    if image_file and allowed_file(image_file.filename):
        # Generate a unique filename
        filename = str(uuid.uuid4()) + '.' + get_file_extension(image_file.filename)

        # Save original image
        original_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        image_file.save(original_path)

        # Resize image if it's too large
        img = Image.open(original_path)
        img.thumbnail((1600, 1200))  # Resize to max 1600x1200 while maintaining aspect ratio
        img.save(original_path, optimize=True, quality=85)

        # Create thumbnail
        thumbnail_filename = f"thumb_{filename}"
        thumbnail_path = os.path.join(current_app.config['UPLOAD_FOLDER'], thumbnail_filename)
        img.thumbnail((200, 200))  # Create a 200x200 thumbnail
        img.save(thumbnail_path)

        # Store paths in database
        store_image_paths(item_id, original_path, thumbnail_path)

        return original_path, thumbnail_path
    return None, None

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_file_extension(filename):
    return filename.rsplit('.', 1)[1].lower()

def store_image_paths(item_id, original_path, thumbnail_path):
    try:
        # Query the item by its ID
        item = Item.query.get(item_id)

        if item:
            # Get the relative path from the uploads folder
            uploads_folder = os.path.join(app.config['STATIC_FOLDER'], 'uploads')
            original_relative = os.path.relpath(original_path, uploads_folder)
            thumbnail_relative = os.path.relpath(thumbnail_path, uploads_folder)

            # Store the relative paths
            item.image_path = os.path.join('uploads', original_relative)
            item.thumbnail_path = os.path.join('uploads', thumbnail_relative)

            db.session.commit()
            current_app.logger.info(f"Image paths updated for item {item_id}")
        else:
            current_app.logger.warning(f"Item with ID {item_id} not found")

    except Exception as e:
        # Log the error and rollback the session
        current_app.logger.error(f"Error updating image paths for item {item_id}: {str(e)}")
        db.session.rollback()
        raise

    return item is not None

@app.errorhandler(413)
def too_large(e):
    return apology("file is too big", 413)

@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory('/workspaces/39122230/final_project/static/', filename)
