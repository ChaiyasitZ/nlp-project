import React, { useEffect, useState } from 'react';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

const Timeline = ({ newsData, onTimelineGenerated }) => {
  const [timelineData, setTimelineData] = useState(null);
  const [selectedEvent, setSelectedEvent] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    if (newsData) {
      generateTimeline();
    }
  }, [newsData]);

  const generateTimeline = async () => {
    setIsLoading(true);
    try {
      // Mock timeline generation - replace with actual API call
      const mockTimeline = {
        events: [
          {
            id: 1,
            date: '2024-01-15',
            title: 'Breaking News Event 1',
            description: 'Important political development occurred',
            entities: ['Person A', 'Organization B', 'Location C'],
            sources: ['Source 1', 'Source 2']
          },
          {
            id: 2,
            date: '2024-01-16',
            title: 'Follow-up News Event',
            description: 'Continuation of previous event with new developments',
            entities: ['Person A', 'Organization D'],
            sources: ['Source 2', 'Source 3']
          },
          {
            id: 3,
            date: '2024-01-17',
            title: 'Related Event',
            description: 'Related development in the same topic',
            entities: ['Person B', 'Organization B'],
            sources: ['Source 1', 'Source 4']
          }
        ],
        chart_data: {
          labels: ['2024-01-15', '2024-01-16', '2024-01-17'],
          datasets: [
            {
              label: 'Event Intensity',
              data: [3, 5, 4],
              borderColor: 'rgb(59, 130, 246)',
              backgroundColor: 'rgba(59, 130, 246, 0.1)',
              tension: 0.4
            }
          ]
        }
      };

      setTimelineData(mockTimeline);
      onTimelineGenerated(mockTimeline);
    } catch (error) {
      console.error('Error generating timeline:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const chartOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: 'News Events Timeline',
      },
    },
    scales: {
      y: {
        beginAtZero: true,
        title: {
          display: true,
          text: 'Event Intensity'
        }
      },
      x: {
        title: {
          display: true,
          text: 'Date'
        }
      }
    },
    onClick: (event, elements) => {
      if (elements.length > 0) {
        const index = elements[0].index;
        setSelectedEvent(timelineData.events[index]);
      }
    }
  };

  if (isLoading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (!timelineData) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-500">No timeline data available</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Timeline Chart */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-4">
          News Events Timeline
        </h2>
        <div className="h-64">
          <Line data={timelineData.chart_data} options={chartOptions} />
        </div>
      </div>

      {/* Events List */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h3 className="text-xl font-bold text-gray-900 mb-4">
          Timeline Events
        </h3>
        <div className="space-y-4">
          {timelineData.events.map((event) => (
            <div
              key={event.id}
              className={`border rounded-lg p-4 cursor-pointer transition-colors ${
                selectedEvent?.id === event.id
                  ? 'border-blue-500 bg-blue-50'
                  : 'border-gray-200 hover:border-gray-300'
              }`}
              onClick={() => setSelectedEvent(event)}
            >
              <div className="flex justify-between items-start mb-2">
                <h4 className="text-lg font-semibold text-gray-900">
                  {event.title}
                </h4>
                <span className="text-sm text-gray-500">
                  {event.date}
                </span>
              </div>
              <p className="text-gray-700 mb-3">
                {event.description}
              </p>
              <div className="flex flex-wrap gap-2 mb-2">
                <span className="text-sm font-medium text-gray-600">
                  Entities:
                </span>
                {event.entities.map((entity, index) => (
                  <span
                    key={index}
                    className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800"
                  >
                    {entity}
                  </span>
                ))}
              </div>
              <div className="flex flex-wrap gap-2">
                <span className="text-sm font-medium text-gray-600">
                  Sources:
                </span>
                {event.sources.map((source, index) => (
                  <span
                    key={index}
                    className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800"
                  >
                    {source}
                  </span>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Selected Event Details */}
      {selectedEvent && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-xl font-bold text-gray-900 mb-4">
            Event Details
          </h3>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <h4 className="font-semibold text-gray-900 mb-2">
                {selectedEvent.title}
              </h4>
              <p className="text-gray-700 mb-3">
                {selectedEvent.description}
              </p>
              <p className="text-sm text-gray-500">
                Date: {selectedEvent.date}
              </p>
            </div>
            <div>
              <h5 className="font-semibold text-gray-900 mb-2">
                Key Entities
              </h5>
              <ul className="list-disc list-inside text-gray-700 mb-3">
                {selectedEvent.entities.map((entity, index) => (
                  <li key={index}>{entity}</li>
                ))}
              </ul>
              <h5 className="font-semibold text-gray-900 mb-2">
                News Sources
              </h5>
              <ul className="list-disc list-inside text-gray-700">
                {selectedEvent.sources.map((source, index) => (
                  <li key={index}>{source}</li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Timeline;
