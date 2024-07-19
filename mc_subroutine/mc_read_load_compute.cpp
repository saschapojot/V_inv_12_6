//
// Created by polya on 7/19/24.
//

#include "mc_read_load_compute.hpp"

///
/// @param x
/// @param leftEnd
/// @param rightEnd
/// @param eps
/// @return return a value within distance eps from x, on the open interval (leftEnd, rightEnd)
double mc_computation::generate_uni_open_inteval(const double &x, const double &leftEnd, const double &rightEnd, const double &eps){


double xMinusEps=x-eps;
double xPlusEps=x+eps;

double unif_left_end=xMinusEps<leftEnd?leftEnd:xMinusEps;
double unif_right_end=xPlusEps>rightEnd?rightEnd:xPlusEps;
//    std::cout << std::setprecision(std::numeric_limits<double>::max_digits10);
//std::cout<<"x="<<x<<std::endl;
//std::cout<<"unif_left_end="<<unif_left_end<<std::endl;
//std::cout<<"unif_right_end="<<unif_right_end<<std::endl;
    std::random_device rd;
    std::ranlux24_base e2(rd());
// in std::uniform_real_distribution<> distUnif(a,b), the random numbers are from interval [a, b)
//we need random numbers from interval (a,b)
double unif_left_end_double_on_the_right=std::nextafter(unif_left_end, std::numeric_limits<double>::infinity());
//    std::cout<<"unif_left_end_double_on_the_right="<<unif_left_end_double_on_the_right<<std::endl;



    std::uniform_real_distribution<> distUnif(unif_left_end_double_on_the_right,unif_right_end); //[unif_left_end_double_on_the_right, unif_right_end)

    double xNext=distUnif(e2);
    return xNext;



}

///
/// @param LCurr current value of L
/// @param y0Curr current value of y0
/// @param z0Curr current value of z0
/// @param y1Curr current value of y1
/// @param LNext  next value of L
/// @param y0Next next value of y0
/// @param z0Next next value of z0
/// @param y1Next next value of y1
void mc_computation::proposal(const double &LCurr, const double& y0Curr,const double& z0Curr, const double& y1Curr,
              double & LNext, double & y0Next, double & z0Next, double & y1Next){

    double eps=potFuncPtr->get_eps();
    double lm=potFuncPtr->getLm();

    y0Next= generate_uni_open_inteval(y0Curr,0,LCurr,eps);
    z0Next= generate_uni_open_inteval(z0Curr,0,LCurr,eps);
    y1Next= generate_uni_open_inteval(y1Curr,0,LCurr,eps);

    LNext= generate_uni_open_inteval(LCurr,y0Next+z0Next+y1Next,lm,eps);




}


///
/// @param LCurr
/// @param y0Curr
/// @param z0Curr
/// @param y1Curr
/// @param LNext
/// @param y0Next
/// @param z0Next
/// @param y1Next
/// @param UNext
/// @return
double mc_computation::acceptanceRatio(const double &LCurr,const double &y0Curr,
                       const double &z0Curr, const double& y1Curr,const double& UCurr,
                       const double &LNext, const double& y0Next,
                       const double & z0Next, const double & y1Next,
                       double &UNext){

    UNext=((*potFuncPtr)(LNext,y0Next,z0Next,y1Next));
    double numerator = -this->beta*UNext;

    double denominator=-this->beta*UCurr;


}