//
// Created by polya on 7/22/24.
//
#include "gen_mc.hpp"

///proportional to probability, target mc distribution
double gen_data::g(const double &x) {

    if (x <= a or x >= b) {
        return 0;
    } else {
        double val = -(x - a) * (x - b);

        return val;

    }

}

///
/// @param y
/// @param x center
/// @return known proposal function, which is normal distribution on R
double gen_data::Q(const double &y, const double &x){

    double val=1/(std::pow(2.0*PI,0.5)*sgm)
               *std::exp(-1/(2*std::pow(sgm,2))*std::pow(y-x,2.0));

    return val;


}


///
/// @param x center
/// @return random number from truncated Gaussian
double gen_data::reject_sampling_one_data(const double &x){

    std::random_device rd;  // Create a random device object
    std::ranlux24_base engine(rd());  // Seed the engine with the random device

    std::normal_distribution<> normal_dist(x,sgm);
    std::uniform_real_distribution<> distUnif01(0, 1);//[0,1)

    double y=normal_dist(engine);
    double u=distUnif01(engine);

    while(u>= f(y,x)/(M* Q(y,x))){
        y=normal_dist(engine);
        u=distUnif01(engine);
    }

    return y;


}

///
/// @param y
/// @param x center
/// @return truncated Gaussian
double gen_data::f(const double &y, const double& x){
    if(y<=a or y>=b){
        return 0;
    }else{

        double val=std::exp(-1.0/(2.0*std::pow(sgm,2))*std::pow(y-x,2));
        return val;
    }




}


///
/// @param xCurr
/// @param xNext
/// @return
void gen_data::proposal(const double &xCurr, double &xNext) {
    xNext = reject_sampling_one_data(xCurr);


}


///
/// @param xCurr
/// @param xNext
/// @return
double  gen_data::acceptanceRatio(const double &xCurr, const double &xNext) {

    double zCurr = zVal(xCurr);
    double zNext = zVal(xNext);

    double R = g(xNext) / g(xCurr) * zCurr / zNext;

    return std::min(1.0, R);


}


///
/// @param x center
/// @return integral
double gen_data::zVal(const double& x){

    auto integrandWithParam=[x, this](const double &y){
        return this->integrand(y,x);
    };
    double result = boost::math::quadrature::trapezoidal(integrandWithParam,a,b);

    return result;

}


///
/// @param y
/// @param x center
/// @return
double gen_data::integrand(const double &y, const double& x){

    return f(y,x);

}

void gen_data::execute_mc(const double& x){

    double xCurr=x;
    std::random_device rd;
    std::ranlux24_base e2(rd());
    std::uniform_real_distribution<> distUnif01(0, 1);//[0,1)

    size_t loopStart=0;

    for (size_t fls = 0; fls < newFlushNum; fls++) {
        const auto tMCStart{std::chrono::steady_clock::now()};
        for (size_t j = 0; j < loopToWrite; j++) {
            //propose a move
            double xNext;
            this->proposal(xCurr,xNext);
            double r= acceptanceRatio(xCurr,xNext);
            double u = distUnif01(e2);
            if (u <= r) {
                xCurr=xNext;

            }//end of accept-reject
            dataAll[j]=xCurr;


        }//end for loop
        size_t loopEnd = loopStart + loopToWrite - 1;
        std::string fileNameMiddle = "loopStart" + std::to_string(loopStart) + "loopEnd" + std::to_string(loopEnd);
        std::string out_FileName = this->dataDir + "/" + fileNameMiddle + ".x.csv";

        saveArrayToCSV(dataAll,loopToWrite,out_FileName);
        const auto tMCEnd{std::chrono::steady_clock::now()};
        const std::chrono::duration<double> elapsed_secondsAll{tMCEnd - tMCStart};
        std::cout << "loop " + std::to_string(loopStart) + " to loop " + std::to_string(loopEnd) + ": "
                  << elapsed_secondsAll.count() / 3600.0 << " h" << std::endl;

        loopStart = loopEnd + 1;
    }//end flush for loop
    std::cout<<"mc executed for "<<newFlushNum<<" flushes."<<std::endl;
}



void gen_data::saveArrayToCSV(const std::shared_ptr<double[]>& array, const  size_t& arraySize, const std::string& filename){
    std::ofstream outFile(filename);

    if (!outFile.is_open()) {
        std::cerr << "Error opening file: " << filename << std::endl;
        return;
    }
    outFile << std::setprecision(std::numeric_limits<double>::digits10 + 1) << std::fixed;
    outFile<<"x_data"<<"\n";
    for(size_t i=0;i<arraySize;i++){
        outFile<<array[i]<<"\n";

    }
    outFile.close();


}
void gen_data::init_and_run(){

    this->execute_mc(xInit);
}
