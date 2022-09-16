import React, { Component } from 'react'
import { MDBContainer, MDBRow, MDBCol } from "mdb-react-ui-kit"
import { connect } from 'react-redux'
import PropTypes from 'prop-types'
import { fetchLib, fetchData } from '../Redux/Actions/SeatActions'
import Card from '../components/Card'


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
        ]
    }

    componentDidMount() {
        this.props.fetchLib();
        this.interval = setInterval(() => {this.props.fetchData()}, 1000);
    }

    // componentDidUpdate(prevProps, prevState) {
    //     console.log('fetched success')
    //     console.log(this.props.data)
    // }

    componentWillUnmount() {
        clearInterval(this.interval)
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
                                    <Card post={lib} vacancy={this.props.vacancy} />
                                </MDBCol>
                            )
                        })}
                    </MDBRow>
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