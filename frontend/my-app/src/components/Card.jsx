import React from "react";
import {
  MDBBtn,
  MDBCard,
  MDBCardBody,
  MDBCardImage,
  MDBCardTitle,
  MDBCardText,
  MDBCol,
  MDBRipple,
  MDBCardHeader,
  MDBIcon,
} from "mdb-react-ui-kit";

const Card = ({ post, vacancy, onClick }) => {
  let availability = post.capacity - Object.entries(vacancy).filter((each) => each[0] === post.id)[0][1]
  let vacancyPercentage = (availability / post.capacity) * 100;
  let color = vacancyPercentage > 50 ? "success" : vacancyPercentage > 25 ? "warning" : "danger";
  return (
    <MDBCol>
      <MDBCard background={color} shadow="0" className="mb-3">
        <MDBCardHeader className="text-white">
        {post.name}
        </MDBCardHeader>
        <MDBCardBody className="text-white">
          <MDBCardTitle className="text-white d-flex align-items-center h1"> {` ${availability} / ${post.capacity}`}
          <MDBBtn outline color="white" className="ms-3 p-2 pt-1 pb-1" size="sm" onClick={() => onClick()} ><i className="bi bi-search"/></MDBBtn>
          </MDBCardTitle>
          <MDBCardText>
          <i className="bi bi-geo-alt me-2"/>{post.location}
          </MDBCardText>
        </MDBCardBody>
      </MDBCard>
    </MDBCol>
  );
};
export default React.memo(Card);
