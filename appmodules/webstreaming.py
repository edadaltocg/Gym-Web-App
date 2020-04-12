import cv2
import gym

def generate():
    env = gym.make('Pong-v0')
    env.reset()
    while True:

        frame, r, d, _ = env.step(env.action_space.sample())
        if d:
            break

        # encode the frame in JPEG format
        (flag, encodedImage) = cv2.imencode(".jpg", frame)
        # ensure the frame was successfully encoded
        if not flag:
            continue

        # yield the output frame in the byte format
        # serve the encoded JPEG frame as a byte array that can be consumed
        # by a web browser.
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
               bytearray(encodedImage) + b'\r\n')

    env.close()
