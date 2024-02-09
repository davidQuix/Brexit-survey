import { Component, ElementRef, OnInit, ViewChild } from '@angular/core';
import { ArcElement, CategoryScale, Chart, ChartConfiguration, Legend, LineController, LineElement, LinearScale, PieController, PointElement, Tooltip } from 'chart.js';

@Component({
  selector: 'app-pie-chart',
  templateUrl: './pie-chart.component.html',
  styleUrls: ['./pie-chart.component.scss']
})
export class PieChartComponent implements OnInit {
  @ViewChild('canvas', { static: true }) canvas: ElementRef<HTMLCanvasElement>;
  chart: Chart;
  configuration: ChartConfiguration = {
    type: 'pie',
    data: {
      labels: ["Support", "Oppose", "Neutral"],
      datasets: [{
        backgroundColor: ["#FF0000", "#0000FF", "#999999"],
        data: [418, 434, 100]
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: {
          position: 'top',
        },
        title: {
          display: true,
          text: 'Chart.js Pie Chart'
        }
      }
    }
  }

  constructor() {
    Chart.register(
      PieController,
      ArcElement,
      Legend,
      Tooltip
    );
  }

  ngOnInit(): void {
    const ctx = this.canvas.nativeElement.getContext('2d');
    this.chart = new Chart(ctx!, this.configuration);
  }
}
