#include "./mc_subroutine/mc_read_load_compute.hpp"
#include "./potentialFunction/potentialFunctionPrototype.hpp"

int main(int argc, char *argv[]) {
    if (argc != 2) {
        std::cout << "wrong arguments" << std::endl;
        std::exit(2);
    }
    auto mcObj=mc_computation(std::string(argv[1]));

//    double LCurr;
//    double y0Curr;
//    double z0Curr;
//    double y1Curr;
//    double LNext;
//    double y0Next;
//    double z0Next;
//    double y1Next;
//    mcObj.proposal(LCurr,y0Curr,z0Curr,y1Curr,LNext,y0Next,z0Next,y1Next);



//    double b = 1.0;
//    std::cout << std::setprecision(std::numeric_limits<double>::digits10 + 1);
//    // Get the closest double value smaller than b
//    double b_minus_epsilon = std::nextafter(b, -std::numeric_limits<double>::infinity());
//    std::cout<<"b_minus_epsilon="<<b_minus_epsilon<<std::endl;


}