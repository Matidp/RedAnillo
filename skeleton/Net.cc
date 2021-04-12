#ifndef NET
#define NET

#include <string.h>
#include <omnetpp.h>
#include <packet_m.h>

using namespace omnetpp;

class Net: public cSimpleModule {
private:
    long pktCounter;
    cOutVector paquetesProcesados;
public:
    Net();
    virtual ~Net();
protected:
    virtual void initialize();
    virtual void finish();
    virtual void handleMessage(cMessage *msg);
};

Define_Module(Net);

#endif /* NET */

Net::Net() {
}

Net::~Net() {
}

void Net::initialize() {
    pktCounter = 0;
    paquetesProcesados.setName("PaquetesProcesados");
    paquetesProcesados.record(0);
}

void Net::finish() {
}

void Net::handleMessage(cMessage *msg) {

    // All msg (events) on net are packets
    Packet *pkt = (Packet *) msg;
    pktCounter++;
    paquetesProcesados.record(pktCounter);

    // If this node is the final destination, send to App
    if (pkt->getDestination() == this->getParentModule()->getIndex()) {
        send(msg, "toApp$o");
    }
    // If not, forward the packet to some else... to who?
    else {
        pkt->setHopCount(pkt->getHopCount()+1);
        send(msg, "toLnk$o", 0);
    }
}
