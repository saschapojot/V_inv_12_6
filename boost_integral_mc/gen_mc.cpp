//
// Created by polya on 7/22/24.
//
#include "gen_mc.hpp"

///proportional to probability
double gen_data::f(const double &x){

double val=-(x-this->a)*(x-this->b);
    return val;

}