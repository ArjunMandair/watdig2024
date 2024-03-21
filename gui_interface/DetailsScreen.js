import React, {useState, useEffect} from 'react';
import { Button, View, StyleSheet } from 'react-native';
import CoordinateTest from './CoordinateTest';
import { ScrollView } from 'react-native-gesture-handler';


function DetailsScreen() {
  const [startButtonText, setStartButtonText] = useState('START');
  const [shutdownButtonText, setShutdownButtonText] = useState('SHUTDOWN');
  const [startButtonColor, setStartButtonColor] = useState();
  const [shutdownButtonColor, setShutdownButtonColor] = useState();
  

  const onPressStartHandler = async () => {
    setStartButtonText('START');
    setStartButtonColor('green');

  };

  const onPressShutdownHandler = async () => {
    setShutdownButtonText('SHUTDOWN CONFIRMED');
    setShutdownButtonColor('red');

  };


  return (
    <ScrollView contentContainerStyle={styles.scrollView}>
      <ScrollView horizontal>
        <View style={styles.container}>
          <View>
            <Button
              title={startButtonText}
              onPress={onPressStartHandler}
              color={startButtonColor}
            />
          </View>
          <View>
            <Button
              title={shutdownButtonText}
              onPress={onPressShutdownHandler}
              color={shutdownButtonColor}
            />
          </View>
          <View>
            <CoordinateTest />
          </View>
        </View>
      </ScrollView>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  scrollView: {
    flexGrow: 1,
  },
  container: {
    justifyContent: 'center',
    alignItems: 'center'
  }
});

export default DetailsScreen;