#ifndef APP
#define APP

#include <string.h>
#include <omnetpp.h>
#include <packet_m.h>

using namespace omnetpp;

class App: public cSimpleModule {
private:
    cMessage *sendMsgEvent;
    cStdDev delayStats;
    cOutVector con_0_delayVector;
    cOutVector con_1_delayVector;
    cOutVector con_2_delayVector;
    cOutVector con_3_delayVector;
    cOutVector con_4_delayVector;
    cOutVector con_6_delayVector;
    cOutVector con_7_delayVector;
    cOutVector generalDelay;
    cOutVector hopCountVector;
    cOutVector sourcesVector;
public:
    App();
    virtual ~App();
protected:
    virtual void initialize();
    virtual void finish();
    virtual void handleMessage(cMessage *msg);
};

Define_Module(App);

#endif /* APP */

App::App() {
}

App::~App() {
}

void App::initialize() {

    // If interArrivalTime for this node is higher than 0
    // initialize packet generator by scheduling sendMsgEvent
    if (par("interArrivalTime").doubleValue() != 0) {
        sendMsgEvent = new cMessage("sendEvent");
        scheduleAt(par("interArrivalTime"), sendMsgEvent);
    }
    generalDelay.setName("General Delay");
    generalDelay.record(0);

    if(this->getParentModule()->getIndex() == 5){

        con_0_delayVector.setName("connection 0 delay");
        con_1_delayVector.setName("connection 1 delay");
        con_2_delayVector.setName("connection 2 delay");
        con_3_delayVector.setName("connection 3 delay");
        con_4_delayVector.setName("connection 4 delay");
        con_6_delayVector.setName("connection 6 delay");
        con_7_delayVector.setName("connection 7 delay");
        con_0_delayVector.record(0);
        con_1_delayVector.record(0);
        con_2_delayVector.record(0);
        con_3_delayVector.record(0);
        con_4_delayVector.record(0);
        con_6_delayVector.record(0);
        con_7_delayVector.record(0);
    }

    // Initialize statistics
    delayStats.setName("TotalDelay");
    hopCountVector.setName("Hop Count");
    hopCountVector.record(0);
    sourcesVector.setName("Source Node");
    sourcesVector.record(0);
}

void App::finish() {
    // Record statistics
    recordScalar("Average delay", delayStats.getMean());
    recordScalar("Number of packets", delayStats.getCount());
}

void App::handleMessage(cMessage *msg) {

    // if msg is a sendMsgEvent, create and send new packet
    if (msg == sendMsgEvent) {
        // create new packet
        Packet *pkt = new Packet("packet",this->getParentModule()->getIndex() +1);
        pkt->setByteLength(par("packetByteSize"));
        pkt->setSource(this->getParentModule()->getIndex());
        pkt->setDestination(par("destination"));

        // send to net layer
        send(pkt, "toNet$o");

        // compute the new departure time and schedule next sendMsgEvent
        simtime_t departureTime = simTime() + par("interArrivalTime");
        scheduleAt(departureTime, sendMsgEvent);

    }
    // else, msg is a packet from net layer
    else {
        // compute delay and record statistics
        Packet *pkt = (Packet *) msg;
        simtime_t delay = simTime() - msg->getCreationTime();

        switch(pkt->getSource()){
            case(0):
                con_0_delayVector.record(delay);
                break;
            case(1):
                con_1_delayVector.record(delay);
                break;
            case(2):
                con_2_delayVector.record(delay);
                break;
            case(3):
                con_3_delayVector.record(delay);
                break;
            case(4):
                con_4_delayVector.record(delay);
                break;
            case(6):
                con_6_delayVector.record(delay);
                break;
            case(7):
                con_7_delayVector.record(delay);
                break;
            default:
                break;

        }
        delayStats.collect(delay);
        generalDelay.record(delay);
        hopCountVector.record(pkt->getHopCount());
        sourcesVector.record(pkt->getSource());
        // delete msg
        delete (msg);
    }

}
