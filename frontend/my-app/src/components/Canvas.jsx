import { MDBBtn, MDBSpinner } from "mdb-react-ui-kit";
import React from "react";
import { useEffect } from "react";
import emailjs from "@emailjs/browser";

const Canvas = ({ data, toggleModal }) => {
  let coord = data.coord.map((seat) => {
    //find center of seat, based on 1920x1080
    return { x: (seat.xmax + seat.xmin) / 2, y: (seat.ymax + seat.ymin) / 2 };
  });
  let seats = data.seats;

  const registerEmail = (e) => {
    //registering for 1 seat
    localStorage.setItem("seat", e.target.value);
    toggleModal();
  };

  const sendEmail = () => {
    const templateParams = {
      to_email: localStorage.getItem("email"),
    };

    emailjs
      .send(
        "service_c00esuj",
        "template_3lru6cq",
        templateParams,
        "Q0gbVPlA6nwjK2Us9"
      )
      .then(
        (response) => {
          console.log("SUCCESS!", response.status, response.text);
        },
        (err) => {
          console.log("FAILED...", err);
        }
      );
  };

  useEffect(() => {
    let monitoredSeat = localStorage.getItem("seat");
    if (monitoredSeat && localStorage.getItem("email")) {
      if (seats[monitoredSeat] === 0) {
        //if vacant
        sendEmail();
        localStorage.removeItem("seat");
        localStorage.removeItem("email");
      }
    }
  }, [coord, seats]);
  return (
    <div>
      <h3 className="text-center">Layout</h3>
      <br />
      <div
        className="square border border-success rounded mx-auto col-md-6 mb-3"
        style={{ position: "relative", height: "30vh" }}
      >
        {coord ? (
          coord.map((seat, index) => {
            return (
              <MDBBtn
                key={index}
                value={index}
                style={{
                  position: "absolute",
                  left: `${(seat.x / 1920) * 100}%`,
                  top: `${(seat.y / 1080) * 100}%`,
                  width: "15px",
                  height: "40px",
                  backgroundColor: seats[index] ? "red" : "green",
                }}
                onClick={registerEmail}
              ></MDBBtn>
            );
          })
        ) : (
          <MDBSpinner
            className="mx-auto"
            style={{ width: "3rem", height: "3rem" }}
          >
            <span className="visually-hidden">Loading...</span>
          </MDBSpinner>
        )}
      </div>
    </div>
  );
};

export default React.memo(Canvas);
