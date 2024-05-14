import React, { Component } from "react";
import CanvasJSReact from "@canvasjs/react-charts";

var CanvasJS = CanvasJSReact.CanvasJS;
var CanvasJSChart = CanvasJSReact.CanvasJSChart;

class App extends Component {
  render() {
    const energyConsumptionGraph = {
      animationEnabled: true,
      exportEnabled: true,
      theme: "light1",
      title: {
        text: "Energy Consumption",
      },
      axisY: {
        title: "Kilowatts",
        suffix: "KW",
      },
      axisX: {
        title: "Day of the Week",
        labelFormatter: function (e) {
          const days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];
          return days[e.value];
        },
      },
      data: [
        {
          type: "line",
          toolTipContent: "Day {x}: {y}KW",
          dataPoints: [
            { x: 1, y: 180.076 },
            { x: 2, y: 204.01 },
            { x: 3, y: 199.2 },
            { x: 4, y: 187.472 },
            { x: 5, y: 139.75 },
            { x: 6, y: 181.032 },
            { x: 7, y: 122.488 },
          ],
        },
      ],
    };

    const SolarVsEskom = {
      
    }

    return (
      <div
        style={{
          display: "flex",
          flexDirection: "column",
          alignItems: "flex-start",
          justifyContent: "flex-start",
          padding: "100px",
          width: "80%",
          height: "300px",
          marginTop: "-50px",
        }}
      >
        <CanvasJSChart options={energyConsumptionGraph} />

        <div
          style={{
            position: "absolute",
            bottom: 30,
            left: 75,
            padding: "20px",
            height: "200px",
            marginTop: "50px",
          }}
        >
          <CanvasJSChart options={energyConsumptionGraph} />

          <div
            style={{
              position: "absolute",
              bottom: 0,
              right: -600,
              padding: "20px",
              height: "200px",
              marginTop: "50px",
            }}
          >
            <CanvasJSChart options={energyConsumptionGraph} />
          </div>
        </div>
      </div>
    );
  }
}

export default App;
