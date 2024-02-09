import { Component, ElementRef, Input, OnInit, ViewChild } from '@angular/core';
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
      labels: [],
      datasets: [{
        backgroundColor: ["#FF0000", "#0000FF", "#999999"],
        data: []
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

  @Input() set labels(labels: string[]) {
    this.configuration.data.labels = labels;
  }
  @Input() set data(data: number[]) {
    console.log(data)
    this.configuration.data.datasets[0].data = data;
    this.chart.update();
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
