import React, { Component } from 'react'
import { MDBContainer, MDBRow, MDBCol } from "mdb-react-ui-kit"
import { connect } from 'react-redux'
import PropTypes from 'prop-types'
import { fetchLib, fetchData } from '../Redux/Actions/SeatActions'
import Card from '../components/Card'
import Canvas from '../components/Canvas'
import Modal from '../components/Modal'


class Home extends Component {
    state = {
        library: [
            {
                name: 'Art, Design and Media Library',
                capacity: 130,
                id: 'ADML',
                location:'ART-01-03'
            },
            {
                name: 'Business Library',
                capacity: 465,
                id: 'BUSL',
                location: 'N2-B2b-07'
            },
            {
                name: 'Chinese Library',
                capacity: 140,
                id: 'CHNL',
                location:'S3.2-B5-01'
            },
            {
                name: 'Communication and Information Library',
                capacity: 60,
                id: 'CMIL',
                location:'CS-01-18'
            },
            {
                name: 'Humanities and Social Sciences Library',
                capacity: 50,
                id: 'HSSL',
                location:'S4-B3C-05'
            },
            {
                name: 'Lee Wee Nam Library',
                capacity: 1200,
                id: 'LWNL',
                location:'NS3-03-01'
            }
        ],
        showSeats: false,
        showModal:false
    }

    componentDidMount() {
        this.props.fetchLib(); //fetch overall Library vacancy
        this.interval = setInterval(() => {this.props.fetchData()}, 1000); //fetch data from RPI FLASK every 1 second
    }
    // Checks prop values so it doesnt rerender every 1s
    shouldComponentUpdate(nextProps, nextState) {
        if (JSON.stringify(this.props.data) !== JSON.stringify(nextProps.data) || JSON.stringify(this.state) !== JSON.stringify(nextState)) {
            return true;
        }
        return false;
    }

    componentWillUnmount() {
        clearInterval(this.interval)
    }

    toggleLayout(){
        this.setState({showSeats: !this.state.showSeats})
    }
    toggleModal = () =>{
        this.setState({showModal: !this.state.showModal})
    }
    render() {
        return (
            <div>
                <MDBContainer>
                    <h1>NTU Library</h1>
                    <h5>View real-time seat availability at our libraries!</h5>
                    <p>Click <a href='https://www.ntu.edu.sg/education/libraries/about-ntu-library' target='_blank' >here</a> for library opening hours and locations.</p>
                    <MDBRow>
                        { this.props.vacancy && this.state.library.map((lib) => {
                            return(
                                <MDBCol lg='4' md='6'>
                                    <Card post={lib} vacancy={this.props.vacancy} onClick={()=> this.toggleLayout()} />
                                </MDBCol>
                            )
                        })}
                    </MDBRow>
                    <MDBRow>
                        {this.state.showSeats && this.props.data && <Canvas data={this.props.data} toggleModal={this.toggleModal} />}
                    </MDBRow>
                    <Modal toggleModal={this.toggleModal} showModal={this.state.showModal} />
                </MDBContainer>
            </div>
        )
    }
}
Home.propTypes = {
    fetchLib: PropTypes.func.isRequired,
    fetchData: PropTypes.func.isRequired
}

const mapStateToProps = state => ({
    vacancy: state.seat.library,
    data: state.seat.data
});

export default connect(mapStateToProps, { fetchLib,fetchData })(Home)