"""
Demonstrates how to use viperdriver to both create a new browser session and connect to an orphan one.
The example should be run twice.
The first execution will create a brand new browser session.
As the result, the session info will be saved in a file.
During the second execution, the script will discover the file and will pass the session info from it to the viperdriver instance.
Then the viperdriver instance will connect to the existing session and will be able to take command of it (in this case hitting a URL and then closing it).
To execute the script: 'python -m viperdriver.examples.conntosession'
"""
from time import sleep
from viperdriver import SessionDriver

def main():
    drv = SessionDriver()
    drv.options.headless = False         # start viperdriver in visible mode

    if drv.session.file_exists():        # if previous session exists, connect to it
        print('Session file found: ' + drv.session.full_path())
        drv.launch(new_session=False)
        print('Will now navigate to Google in:')
        x = range(5)
        for i in x:
            print('\b', x[-1-i], sep='', end='', flush=True)
            sleep(1)
        print('\n')
        drv.get('http://google.com')
        print('Will now close the browser.')
        for i in range(10):
            print('.', sep='', end='', flush=True)
            sleep(0.5)
        print('\n')
        drv.quit()
    else:                               # if session does not exist, create new one and save to file
        drv.launch(new_session=True)
        drv.set_window_size(600, 300)
        drv.session.save_to_file()
        print('Exiting. Please start again.')

if __name__ == '__main__':
    main()
