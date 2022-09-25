import os, sys
import time
from PIL import Image, ImageFont, ImageDraw
from .models import Ticket
from datetime import datetime
import qrcode

# generate a printable ticket with
import payment


def generate_ticket(ticket_info):
    # TODO: Test if it works without absolute path in win/linux

    # open image for tests
    ticket_tmp = Image.open("payment/resources/templates/ticket_tmp.jpg")
    title_font = ImageFont.truetype("payment/resources/fonts/Powerline.ttf", 50)

    # set text
    # date_font = title_font
    # type_text = type

    # draw
    image_editable = ImageDraw.Draw(ticket_tmp)
    # left hand side
    image_editable.text((100, 275), ticket_info["title"], (0, 0, 0), font=title_font)
    image_editable.text((210, 360), ticket_info["certificate"], (0, 0, 0), font=title_font)

    image_editable.text((205, 440), ticket_info["date"], (0, 0, 0), font=title_font)
    image_editable.text((205, 490), ticket_info["time"], (0, 0, 0), font=title_font)
    image_editable.text((250, 540), ticket_info["screen"], (0, 0, 0), font=title_font)

    # right hand side
    image_editable.text((750, 170), ticket_info["ticket_type"], (0, 0, 0), font=title_font)
    image_editable.text((1000, 665), "Row " + ticket_info["seat_row"], (0, 0, 0), font=title_font)
    image_editable.text((1000, 715), "No. " + ticket_info["seat_number"], (0, 0, 0), font=title_font)

    # add qr code
    input_data = "Movie:" + ticket_info["title"] + "; Date:" + ticket_info["date"] + \
                 "; Time" + ticket_info["time"] + "; Row :" + ticket_info["seat_row"] + \
                 "; Seat Number: " + ticket_info["seat_number"]

    qr_image_size = 10
    qr = qrcode.QRCode(
        # error_correction=qrcode.constants.ERROR_CORRECT_H,
        version=1,
        box_size=qr_image_size,
        border=2)
    qr.add_data(input_data)
    qr.make(fit=True)
    qr_img = qr.make_image(fill='black', back_color='white').convert('RGBA')

    # qr_img + ticket_tmp   => ticketImage
    ticketImage = ticket_tmp.copy()
    ticketImage.paste(qr_img, (720, 250))

    # for debugging
    # ticketImage.show()

    ticket_id = ticket_info["ticket_id"]
    path = os.path.dirname(payment.__file__)
    # write pdf
    try:
        ticketImage.save(f"{path}/resources/rendered_tickets/ticket{ticket_id}.pdf")
    except:
        os.remove(f"{path}/resources/rendered_tickets/ticket{ticket_id}.pdf")
        ticketImage.save(f"{path}/resources/rendered_tickets/ticket{ticket_id}.pdf")
    # write image
    try:
        ticketImage.save(f"{path}/resources/rendered_tickets/ticket{ticket_id}.png")
    except:
        os.remove(f"{path}/resources/rendered_tickets/ticket{ticket_id}.png")
        ticketImage.save(f"{path}/resources/rendered_tickets/ticket{ticket_id}.png")


def ticket_info(ticket):
    movie_title = ticket.showtime.movie.title
    certificate = ticket.showtime.movie.certificate
    movie_date = ticket.showtime.time.date().strftime("%m/%d/%Y")
    movie_time = ticket.showtime.time.time().strftime("%H:%M")
    screen = ticket.showtime.hall.name
    ticket_type = ticket.type

    row_number = str(ticket.seat.row_number)
    seat_number = str(ticket.seat.seat_number)

    ticket_id = str(ticket.id)

    return {"title": movie_title,
            "certificate": certificate,
            "date": movie_date,
            "time": movie_time,
            "screen": screen,
            "ticket_type": ticket_type,
            "seat_row": row_number,
            "seat_number": seat_number,
            "ticket_id": ticket_id
            }

# if __name__ == "__main__":
#     # movie_title,rating,movie_date,screen, type,seat, movie_id
#     generate_ticket("TEST MOVIE TITLE", "R18", str(datetime.now()), "hall 2", "ADULT", "A1", 1)
