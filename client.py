import socket, sys, select

def open_connection(host, port):
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.connect((host, port)) #10.1.10.100
    return my_socket

def format_message(msg):
    if "::" in msg:
        message = msg.split("::", 1)
        return "[%s] %s" % (message[0], message[1])
    else:
        return msg 

def main():
    my_socket = open_connection("10.1.10.100", 5555)

    running = True
    while running:
        inputready, outputready, exceptready = select.select([my_socket, sys.stdin], [], [])

        for s in inputready:
            if s == my_socket:
                msg = s.recv(1024)
                if msg:
                    print format_message(msg)
                else:
                    print "Disconnected from server!"
                    running = False
            elif s == sys.stdin:
                user_input = s.readline().rstrip("\n")

                if user_input == "quit":
                    running = False
                else:
                    my_socket.sendall(user_input)

    my_socket.close()

main()