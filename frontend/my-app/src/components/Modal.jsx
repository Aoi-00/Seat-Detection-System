import React, { useState } from "react";
import {
  MDBBtn,
  MDBModal,
  MDBModalDialog,
  MDBModalContent,
  MDBModalHeader,
  MDBModalTitle,
  MDBModalBody,
  MDBModalFooter,
  MDBInput,
  MDBValidationItem,
  MDBValidation,
} from "mdb-react-ui-kit";

const Modal = ({ toggleModal, showModal }) => {
  const [basicModal, setBasicModal] = useState(showModal);
  const [email, setEmail] = useState("");
  const saveEmail = () => {
    if (email.length && email.includes("@")) {
        localStorage.setItem("email", email);
        setEmail("");
        toggleModal();
    }
  };
  return (
    <>
      <MDBModal
        staticBackdrop
        show={showModal}
        setShow={setBasicModal}
        tabIndex="-1"
      >
        <MDBModalDialog>
          <MDBModalContent>
            <MDBModalHeader>
              <MDBModalTitle>Get Email Notification</MDBModalTitle>
              <MDBBtn
                className="btn-close"
                color="none"
                onClick={toggleModal}
              ></MDBBtn>
            </MDBModalHeader>
            <MDBValidation>
            <MDBModalBody>
              <MDBValidationItem feedback="Please enter your email." invalid>
                <MDBInput
                  type="email"
                  className="form-control"
                  id="validationCustomUsername"
                  label="Email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                />
              </MDBValidationItem>
            </MDBModalBody>

            <MDBModalFooter>
              <MDBBtn outline color="danger" type="reset" onClick={toggleModal}>
                Close
              </MDBBtn>
              <MDBBtn outline type="submit" onClick={saveEmail}>
                Save changes
              </MDBBtn>
            </MDBModalFooter>
            </MDBValidation>
          </MDBModalContent>
        </MDBModalDialog>
      </MDBModal>
    </>
  );
};
export default React.memo(Modal);
