import os
import mechanize

def main():
    # Fetch the credentials from environment variables
    username = os.getenv('USERNAME')
    password = os.getenv('PASSWORD')

    # Create a mechanize browser object
    br = mechanize.Browser()

    # Ignore robots.txt
    br.set_handle_robots(False)

    # Open the login page
    br.open('https://www.screener.in/login/')

    # Select the login form
    br.select_form('login-form')

    # Fill in the login credentials
    br.form['username'] = username
    br.form['password'] = password

    # Submit the login form
    response = br.submit()

    # Return the response object
    return response

if __name__ == "__main__":
    response = main()
    print(f"Status Code: {response.getcode()}")
    print(f"Response Text: {response.read()}")
