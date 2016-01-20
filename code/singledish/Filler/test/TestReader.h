/*
 * TestReader.h
 *
 *  Created on: Jan 15, 2016
 *      Author: nakazato
 */

#ifndef SINGLEDISH_FILLER_TEST_TESTREADER_H_
#define SINGLEDISH_FILLER_TEST_TESTREADER_H_

#include <casacore/casa/Arrays/Array.h>
#include <casacore/casa/BasicSL/Constants.h>
#include <casacore/casa/Quanta/MVPosition.h>
#include <casacore/measures/Measures/MPosition.h>
#include <casacore/measures/Measures/MeasConvert.h>

using namespace casa;
using namespace casacore;

class FixedNumberIteratorInterface {
public:
  FixedNumberIteratorInterface(size_t num_iter) :
      num_iter_(num_iter), current_iter_(0) {
  }
  virtual ~FixedNumberIteratorInterface() {
  }

  bool moreData() const {
    return current_iter_ < num_iter_;
  }

  virtual void getEntry(TableRecord &record) = 0;

  void next() {
    ++current_iter_;
  }

protected:
  size_t const num_iter_;
  size_t current_iter_;
};

// Iterator for SOURCE table
class SourceIterator: public FixedNumberIteratorInterface {
public:
  SourceIterator() :
      FixedNumberIteratorInterface(4), source_id_(num_iter_), time_(num_iter_), interval_(
          num_iter_), spectral_window_id_(num_iter_), num_lines_(num_iter_), name_(
          num_iter_), calibration_group_(num_iter_), code_(num_iter_), direction_(
          num_iter_, Vector < Double > (2)), proper_motion_(num_iter_,
          Vector < Double > (2)), transition_(num_iter_), rest_frequency_(
          num_iter_), sysvel_(num_iter_) {
    POST_START;

    source_id_[0] = 0;
    source_id_[1] = 0;
    source_id_[2] = 1;
    source_id_[3] = 1;
    name_[0] = "M78";
    name_[1] = "M78";
    name_[2] = "HLTau";
    name_[2] = "HLTau";
    Time t(2016, 1, 1);
    time_ = t.modifiedJulianDay() * 86400.0;
    time_[2] += 86400.0;
    time_[3] = time_[2];
    interval_ = 3600.0;
    calibration_group_ = -1;
    code_ = "";
    Vector < Double > direction(2, 0.0);
    direction_[0] = direction;
    direction_[1] = direction;
    direction[0] += C::pi;
    direction[1] -= C::pi;
    direction_[2] = direction;
    direction_[3] = direction;
    Vector < Double > proper_motion(direction);
    proper_motion = 0.0;
    proper_motion_[0] = proper_motion;
    proper_motion_[1] = proper_motion;
    proper_motion[0] = 0.1;
    proper_motion[1] = -0.05;
    proper_motion_[2] = proper_motion;
    proper_motion_[3] = proper_motion;
    spectral_window_id_[0] = 0;
    spectral_window_id_[1] = 1;
    spectral_window_id_[2] = 0;
    spectral_window_id_[3] = 1;
    num_lines_[0] = 0;
    num_lines_[1] = 2;
    num_lines_[2] = 0;
    num_lines_[3] = 1;
    transition_[0] = Vector<String>();
    rest_frequency_[0] = Vector<Double>();
    sysvel_[0] = Vector<Double>();
    transition_[1] = Vector < String > (1, "12CO(1-0)");
    rest_frequency_[1] = Vector < Double > (1, 115.271203e9);
    sysvel_[1] = Vector < Double > (1, 10.0);
    transition_[2] = transition_[0];
    rest_frequency_[2] = rest_frequency_[0];
    sysvel_[2] = sysvel_[0];
    transition_[3] = Vector < String > (2);
    transition_[3][0] = "12CO(1-0)";
    transition_[3][1] = "13CO(1-0)";
    rest_frequency_[3] = Vector < Double > (2);
    rest_frequency_[3][0] = 115.271203e9;
    rest_frequency_[3][1] = 110.20137e9;
    sysvel_[3] = Vector < Double > (2, 15.0);

    POST_END;
  }
  ~SourceIterator() {
    POST_START;
    POST_END;
  }

  void getEntry(TableRecord &record) {
    if (moreData()) {
      size_t i = current_iter_;
      record.define("SOURCE_ID", source_id_[i]);
      record.define("NAME", name_[i]);
      record.define("TIME", time_[i]);
      record.define("INTERVAL", interval_[i]);
      record.define("CALIBRATION_GROUP", calibration_group_[i]);
      record.define("CODE", code_[i]);
      record.define("DIRECTION", direction_[i]);
      record.define("PROPER_MOTION", proper_motion_[i]);
      record.define("SPECTRAL_WINDOW_ID", spectral_window_id_[i]);
      record.define("NUM_LINES", num_lines_[i]);
      record.define("TRANSITION", transition_[i]);
      record.define("REST_FREQUENCY", rest_frequency_[i]);
      record.define("SYSVEL", sysvel_[i]);
    }
  }

private:
  Vector<Int> source_id_;
  Vector<Double> time_;
  Vector<Double> interval_;
  Vector<Int> spectral_window_id_;
  Vector<Int> num_lines_;
  Vector<String> name_;
  Vector<Int> calibration_group_;
  Vector<String> code_;
  Vector<Vector<Double> > direction_;
  Vector<Vector<Double> > proper_motion_;
  Vector<Vector<String> > transition_;
  Vector<Vector<Double> > rest_frequency_;
  Vector<Vector<Double> > sysvel_;
};

class SysCalIterator: public FixedNumberIteratorInterface {
public:
  SysCalIterator() :
      FixedNumberIteratorInterface(4), antenna_id_(num_iter_), feed_id_(
          num_iter_), spectral_window_id_(num_iter_), time_(num_iter_), interval_(
          num_iter_), tcal_(num_iter_, Vector<Float>()), tcal_spectrum_(
          num_iter_, Matrix<Float>()), tsys_(num_iter_, Vector<Float>()), tsys_spectrum_(
          num_iter_, Matrix<Float>()) {
    antenna_id_[0] = 0;
    antenna_id_[1] = 0;
    antenna_id_[2] = 3;
    antenna_id_[3] = 3;
    feed_id_[0] = 0;
    feed_id_[1] = 1;
    feed_id_[2] = 2;
    feed_id_[3] = 1;
    spectral_window_id_[0] = 0;
    spectral_window_id_[1] = 1;
    spectral_window_id_[2] = 0;
    spectral_window_id_[3] = 1;
    Time t(2016, 1, 1);
    time_ = t.modifiedJulianDay() * 86400.0;
    time_[2] += 86400.0;
    time_[3] = time_[2];
    interval_ = 3600.0;
    tcal_[0] = Vector < Float > (2, 100.0);
    tcal_[1] = Vector<Float>();
    tcal_[2] = tcal_[1];
    tcal_[3] = tcal_[0] * 2.0f;
    tsys_[0] = Vector<Float>();
    tsys_[1] = tsys_[0];
    tsys_[2] = Vector < Float > (1, 150.0);
    tsys_[3] = tsys_[2];
    tcal_spectrum_[0] = Matrix<Float>();
    tcal_spectrum_[1] = Matrix < Float > (IPosition(2, 128), 175.0);
    tcal_spectrum_[2] = tcal_spectrum_[0];
    tcal_spectrum_[3] = tcal_spectrum_[1];
    tsys_spectrum_[0] = Matrix<Float>();
    tsys_spectrum_[1] = tsys_spectrum_[0];
    tsys_spectrum_[2] = Matrix < Float > (IPosition(2, 64), 240.0);
    tsys_spectrum_[3] = tsys_spectrum_[2];
  }

  virtual ~SysCalIterator() {
  }

  void getEntry(TableRecord &record) {
    if (moreData()) {
      size_t i = current_iter_;
      record.define("ANTENNA_ID", antenna_id_[i]);
      record.define("FEED_ID", feed_id_[i]);
      record.define("SPECTRAL_WINDOW_ID", spectral_window_id_[i]);
      record.define("TIME", time_[i]);
      record.define("INTERVAL", interval_[i]);
      record.define("TCAL", tcal_[i]);
      record.define("TCAL_SPECTRUM", tcal_spectrum_[i]);
      record.define("TSYS", tsys_[i]);
      record.define("TSYS_SPECTRUM", tsys_spectrum_[i]);
    }
  }

private:
  Vector<Int> antenna_id_;
  Vector<Int> feed_id_;
  Vector<Int> spectral_window_id_;
  Vector<Double> time_;
  Vector<Double> interval_;
  Vector<Vector<Float> > tcal_;
  Vector<Matrix<Float> > tcal_spectrum_;
  Vector<Vector<Float> > tsys_;
  Vector<Matrix<Float> > tsys_spectrum_;
};

class WeatherIterator: public FixedNumberIteratorInterface {
public:
  WeatherIterator() :
      FixedNumberIteratorInterface(2), antenna_id_(num_iter_), time_(num_iter_), interval_(
          num_iter_), temperature_(num_iter_), pressure_(num_iter_), rel_humidity_(
          num_iter_), wind_speed_(num_iter_), wind_direction_(num_iter_) {
    antenna_id_[0] = 0;
    antenna_id_[1] = -1;
    Time t(2016, 1, 1);
    time_[0] = t.modifiedJulianDay() * 86400.0;
    time_[1] += 3600.0;
    interval_ = 3600.0;
    temperature_[0] = 273.0;
    temperature_[1] = 275.2;
    pressure_[0] = 987.0;
    pressure_[1] = 994.6;
    rel_humidity_[0] = 0.2;
    rel_humidity_[1] = 0.15;
    wind_speed_[0] = 20.0;
    wind_speed_[1] = 1.2;
    wind_direction_[0] = 0.0;
    wind_direction_[1] = -C::pi;
  }

  virtual ~WeatherIterator() {
  }

  void getEntry(TableRecord &record) {
    if (moreData()) {
      size_t i = current_iter_;
      record.define("ANTENNA_ID", antenna_id_[i]);
      record.define("TIME", time_[i]);
      record.define("INTERVAL", interval_[i]);
      record.define("TEMPERATURE", temperature_[i]);
      record.define("PRESSURE", pressure_[i]);
      record.define("REL_HUMIDITY", rel_humidity_[i]);
      record.define("WIND_SPEED", wind_speed_[i]);
      record.define("WIND_DIRECTION", wind_direction_[i]);
    }
  }

private:
  Vector<Int> antenna_id_;
  Vector<Double> time_;
  Vector<Double> interval_;
  Vector<Float> temperature_;
  Vector<Float> pressure_;
  Vector<Float> rel_humidity_;
  Vector<Float> wind_speed_;
  Vector<Float> wind_direction_;
};


// Mock object for Reader
class TestReader: public casa::ReaderInterface {
public:
  TestReader(std::string const &name) :
      casa::ReaderInterface(name), source_iterator_(nullptr), syscal_iterator_(
          nullptr), weather_iterator_(nullptr), get_observation_row_(
          &::TestReader::getObservationRowImpl), get_antenna_row_(
          &::TestReader::getAntennaRowImpl), get_processor_row_(
          &::TestReader::getProcessorRowImpl), get_source_row_(
          &::TestReader::getSourceRowWithInitImpl), get_syscal_row_(
          &::TestReader::getSysCalRowWithInitImpl), get_weather_row_(
          &::TestReader::getWeatherRowWithInitImpl) {
    POST_START;
    POST_END;
  }

  ~TestReader() {
    POST_START;
    POST_END;
  }

  // get number of rows
  virtual size_t getNumberOfRows() { return 0; }

  // to get OBSERVATION table
  virtual Bool getObservationRow(TableRecord &record) {
    POST_START;

    Bool return_value = (*this.*get_observation_row_)(record);

    POST_END;
    return return_value;
  }

  // to get ANTENNA table
  virtual Bool getAntennaRow(TableRecord &record) {
    POST_START;

    Bool return_value = (*this.*get_antenna_row_)(record);

    POST_END;

    return return_value;
  }

  // to get PROCESSOR table
  virtual Bool getProcessorRow(TableRecord &record) {
    POST_START;

    Bool return_value = (*this.*get_processor_row_)(record);

    POST_END;
    return return_value;
  }

  // to get SOURCE table
  virtual Bool getSourceRow(TableRecord &record) {
    POST_START;

    Bool return_value = (*this.*get_source_row_)(record);

    POST_END;

    return return_value;
  }

  // to get SYSCAL table
  virtual Bool getSyscalRow(TableRecord &record) {
    POST_START;

    Bool return_value = (*this.*get_syscal_row_)(record);

    POST_END;

    return return_value;
  }

  // to get WEATHER table
  virtual Bool getWeatherRow(TableRecord &record) {
    POST_START;

    Bool return_value = (*this.*get_weather_row_)(record);

    POST_END;

    return return_value;
  }

  // to get MAIN table
  virtual Bool getMainRecord(TableRecord &record) {
    POST_START;
    POST_END;
    return True;
  }

  // for DataAccumulator
  virtual Bool getData(size_t irow, TableRecord &record) {
    POST_START;
    POST_END;
    return True;
  }

  // for testing
  TableRecord observation_record_;
  TableRecord antenna_record_;
  TableRecord processor_record_;
  TableRecord source_record_;
  TableRecord syscal_record_;
  TableRecord weather_record_;
  TableRecord main_record_;

protected:
  void initializeSpecific() {
    POST_START;
    POST_END;
  }

  void finalizeSpecific() {
    POST_START;
    POST_END;
  }

private:
  std::unique_ptr<SourceIterator> source_iterator_;
  std::unique_ptr<SysCalIterator> syscal_iterator_;
  std::unique_ptr<WeatherIterator> weather_iterator_;
  Bool (::TestReader::*get_observation_row_)(TableRecord &);
  Bool (::TestReader::*get_antenna_row_)(TableRecord &);
  Bool (::TestReader::*get_processor_row_)(TableRecord &);
  Bool (::TestReader::*get_source_row_)(TableRecord &);
  Bool (::TestReader::*get_syscal_row_)(TableRecord &);
  Bool (::TestReader::*get_weather_row_)(TableRecord &);

  Bool getObservationRowImpl(TableRecord &record) {
    POST_START;

    record.define("TELESCOPE_NAME", "MyTelescope");
    Vector < Double > time_range(2);
    Time t(2016, 1, 1);
    time_range[0] = t.modifiedJulianDay() * 86400.0; // sec
    t = t + 3600.0;
    time_range[1] = t.modifiedJulianDay();
    std::cout << "MJD=" << time_range[0] << std::endl;
    record.define("TIME_RANGE", time_range);
    record.define("OBSERVER", "MyName");
    record.define("SCHEDULE_TYPE", "ALMA-SD");
    record.define("PROJECT", "MyProject");
    t = t + 86400.0;
    record.define("RELEASE_DATE", t.modifiedJulianDay());
    Vector < String > strvec(1, "");
    record.define("LOG", strvec);
    strvec[0] = "NextSchedule";
    record.define("SCHEDULE", strvec);

    // keep record contents
    observation_record_.assign(record);

    // redirect function pointer to noMoreRowImpl
    get_observation_row_ = &::TestReader::noMoreRowImpl;

    POST_END;

    return True;
  }

  Bool getAntennaRowImpl(TableRecord &record) {
    POST_START;

    record.define("NAME", "PMXY");
    record.define("STATION", "A00");
    record.define("TYPE", "GROUND-BASED");
    record.define("MOUNT", "ALT-AZ");
    MVPosition mvposition(Quantity(5056.8, "m"),
        Quantity(-1.1825465955049892, "rad"),
        Quantity(-0.4018251640113072, "rad"));
    MPosition position(mvposition, MPosition::WGS84);
    Quantum<Vector<Double> > position_val = MPosition::Convert(position,
        MPosition::ITRF)().get("m");
    record.define("POSITION", position_val.getValue());
    MVPosition mvoffset(Quantity(-50.0, "m"), Quantity(0.01, "rad"),
        Quantity(-0.01, "rad"));
    MPosition offset(mvoffset, MPosition::ITRF);
    Quantum<Vector<Double> > offset_val = offset.get("m");
    record.define("OFFSET", offset_val.getValue());
    record.define("DISH_DIAMETER", 12.0);

    // keep record contents
    antenna_record_.assign(record);

    // redirect function pointer to noMoreRowImpl
    get_antenna_row_ = &::TestReader::noMoreRowImpl;

    POST_END;

    return True;
  }

  Bool getProcessorRowImpl(TableRecord &record) {
    POST_START;

    record.define("TYPE", "CORRELATOR");
    record.define("SUB_TYPE", "ACA");
    record.define("TYPE_ID", -1);
    record.define("MODE_ID", 37);

    // keep record contents
    processor_record_.assign(record);

    // redirect function pointer to noMoreRowImpl
    get_processor_row_ = &::TestReader::noMoreRowImpl;

    POST_END;
    return True;
  }

  Bool getSourceRowWithInitImpl(TableRecord &record) {
    POST_START;

    source_iterator_.reset(new ::SourceIterator());
    get_source_row_ = &::TestReader::getSourceRowImpl;

    Bool more_rows = getSourceRowImpl(record);

    POST_END;

    return more_rows;
  }

  Bool getSourceRowImpl(TableRecord &record) {
    POST_START;

    assert(source_iterator_);

    bool more_rows = source_iterator_->moreData();

    if (more_rows) {
      source_iterator_->getEntry(record);
      source_iterator_->next();

      // keep record contents
      uInt i = source_record_.nfields();
      String key = "ROW" + String::toString(i);
      source_record_.defineRecord(key, record);
    } else {
      source_iterator_.reset(nullptr);
      get_source_row_ = &::TestReader::noMoreRowImpl;
    }

    POST_END;

    return more_rows;
  }

  Bool getSysCalRowWithInitImpl(TableRecord &record) {
    POST_START;

    syscal_iterator_.reset(new ::SysCalIterator());
    get_syscal_row_ = &::TestReader::getSysCalRowImpl;

    Bool more_rows = getSysCalRowImpl(record);

    POST_END;

    return more_rows;
  }

  Bool getSysCalRowImpl(TableRecord &record) {
    POST_START;

    assert(syscal_iterator_);

    bool more_rows = syscal_iterator_->moreData();

    if (more_rows) {
      syscal_iterator_->getEntry(record);
      syscal_iterator_->next();

      // keep record contents
      uInt i = syscal_record_.nfields();
      String key = "ROW" + String::toString(i);
      syscal_record_.defineRecord(key, record);
    } else {
      syscal_iterator_.reset(nullptr);
      get_syscal_row_ = &::TestReader::noMoreRowImpl;
    }

    POST_END;

    return more_rows;

  }

  Bool getWeatherRowWithInitImpl(TableRecord &record) {
    POST_START;

    weather_iterator_.reset(new ::WeatherIterator());
    get_weather_row_ = &::TestReader::getWeatherRowImpl;

    Bool more_rows = getWeatherRowImpl(record);

    POST_END;

    return more_rows;
  }

  Bool getWeatherRowImpl(TableRecord &record) {
    POST_START;

    assert(weather_iterator_);

    bool more_rows = weather_iterator_->moreData();

    if (more_rows) {
      weather_iterator_->getEntry(record);
      weather_iterator_->next();

      // keep record contents
      uInt i = weather_record_.nfields();
      String key = "ROW" + String::toString(i);
      weather_record_.defineRecord(key, record);
    } else {
      weather_iterator_.reset(nullptr);
      get_weather_row_ = &::TestReader::noMoreRowImpl;
    }

    POST_END;

    return more_rows;

  }

  Bool noMoreRowImpl(TableRecord &) {
    POST_START;
    POST_END;

    return False;
  }
};

#endif /* SINGLEDISH_FILLER_TEST_TESTREADER_H_ */