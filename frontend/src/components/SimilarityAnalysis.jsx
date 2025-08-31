import React from 'react';
import { Bar, Doughnut } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend
);

const SimilarityAnalysis = ({ similarityData }) => {
  if (!similarityData) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-500">No similarity analysis data available</p>
        <p className="text-sm text-gray-400 mt-2">
          Please run a comparison analysis first
        </p>
      </div>
    );
  }

  // Sentiment Analysis Chart Data
  const sentimentData = {
    labels: ['Positive', 'Neutral', 'Negative'],
    datasets: [
      {
        label: 'Article 1',
        data: [
          similarityData.sentiment_analysis.article1.positive * 100,
          similarityData.sentiment_analysis.article1.neutral * 100,
          similarityData.sentiment_analysis.article1.negative * 100
        ],
        backgroundColor: ['#10B981', '#6B7280', '#EF4444'],
        borderWidth: 2,
        borderColor: '#ffffff'
      },
      {
        label: 'Article 2',
        data: [
          similarityData.sentiment_analysis.article2.positive * 100,
          similarityData.sentiment_analysis.article2.neutral * 100,
          similarityData.sentiment_analysis.article2.negative * 100
        ],
        backgroundColor: ['#059669', '#4B5563', '#DC2626'],
        borderWidth: 2,
        borderColor: '#ffffff'
      }
    ]
  };

  const sentimentOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: 'Sentiment Analysis Comparison (%)',
      },
    },
    scales: {
      y: {
        beginAtZero: true,
        max: 100,
        title: {
          display: true,
          text: 'Percentage'
        }
      }
    }
  };

  // Similarity Score Doughnut Chart
  const similarityChartData = {
    labels: ['Similar Content', 'Different Content'],
    datasets: [
      {
        data: [
          similarityData.similarity_score * 100,
          (1 - similarityData.similarity_score) * 100
        ],
        backgroundColor: ['#3B82F6', '#E5E7EB'],
        borderWidth: 0
      }
    ]
  };

  const similarityChartOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: 'bottom',
      },
      title: {
        display: true,
        text: 'Content Similarity Distribution',
      },
    }
  };

  return (
    <div className="space-y-6">
      {/* Overall Similarity Score */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-6">
          Similarity Analysis Dashboard
        </h2>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
          <div className="text-center">
            <div className="text-4xl font-bold text-blue-600 mb-2">
              {Math.round(similarityData.similarity_score * 100)}%
            </div>
            <div className="text-gray-600">Overall Similarity</div>
          </div>
          <div className="text-center">
            <div className="text-4xl font-bold text-green-600 mb-2">
              {similarityData.common_entities.length}
            </div>
            <div className="text-gray-600">Common Entities</div>
          </div>
          <div className="text-center">
            <div className="text-4xl font-bold text-purple-600 mb-2">
              {similarityData.common_keywords.length}
            </div>
            <div className="text-gray-600">Common Keywords</div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="h-64">
            <Doughnut data={similarityChartData} options={similarityChartOptions} />
          </div>
          <div className="h-64">
            <Bar data={sentimentData} options={sentimentOptions} />
          </div>
        </div>
      </div>

      {/* Detailed Analysis */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Content Differences */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-xl font-bold text-gray-900 mb-4">
            Content Differences
          </h3>
          <div className="space-y-4">
            {similarityData.content_differences.map((diff, index) => (
              <div
                key={index}
                className={`p-4 rounded-lg border-l-4 ${
                  diff.type === 'added'
                    ? 'border-green-500 bg-green-50'
                    : 'border-red-500 bg-red-50'
                }`}
              >
                <div className="flex items-center mb-2">
                  <span
                    className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                      diff.type === 'added'
                        ? 'bg-green-100 text-green-800'
                        : 'bg-red-100 text-red-800'
                    }`}
                  >
                    {diff.type === 'added' ? 'Added in' : 'Only in'} Article {diff.article}
                  </span>
                </div>
                <p className="text-gray-700 text-sm">
                  {diff.text}
                </p>
              </div>
            ))}
          </div>
        </div>

        {/* Sentiment Breakdown */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-xl font-bold text-gray-900 mb-4">
            Sentiment Breakdown
          </h3>
          <div className="space-y-4">
            <div>
              <h4 className="font-semibold text-gray-900 mb-2">Article 1</h4>
              <div className="space-y-2">
                <div className="flex justify-between items-center">
                  <span className="text-sm text-gray-600">Positive</span>
                  <span className="text-sm font-medium text-green-600">
                    {Math.round(similarityData.sentiment_analysis.article1.positive * 100)}%
                  </span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div
                    className="bg-green-500 h-2 rounded-full"
                    style={{ width: `${similarityData.sentiment_analysis.article1.positive * 100}%` }}
                  ></div>
                </div>
                
                <div className="flex justify-between items-center">
                  <span className="text-sm text-gray-600">Neutral</span>
                  <span className="text-sm font-medium text-gray-600">
                    {Math.round(similarityData.sentiment_analysis.article1.neutral * 100)}%
                  </span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div
                    className="bg-gray-500 h-2 rounded-full"
                    style={{ width: `${similarityData.sentiment_analysis.article1.neutral * 100}%` }}
                  ></div>
                </div>
                
                <div className="flex justify-between items-center">
                  <span className="text-sm text-gray-600">Negative</span>
                  <span className="text-sm font-medium text-red-600">
                    {Math.round(similarityData.sentiment_analysis.article1.negative * 100)}%
                  </span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div
                    className="bg-red-500 h-2 rounded-full"
                    style={{ width: `${similarityData.sentiment_analysis.article1.negative * 100}%` }}
                  ></div>
                </div>
              </div>
            </div>

            <div>
              <h4 className="font-semibold text-gray-900 mb-2">Article 2</h4>
              <div className="space-y-2">
                <div className="flex justify-between items-center">
                  <span className="text-sm text-gray-600">Positive</span>
                  <span className="text-sm font-medium text-green-600">
                    {Math.round(similarityData.sentiment_analysis.article2.positive * 100)}%
                  </span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div
                    className="bg-green-500 h-2 rounded-full"
                    style={{ width: `${similarityData.sentiment_analysis.article2.positive * 100}%` }}
                  ></div>
                </div>
                
                <div className="flex justify-between items-center">
                  <span className="text-sm text-gray-600">Neutral</span>
                  <span className="text-sm font-medium text-gray-600">
                    {Math.round(similarityData.sentiment_analysis.article2.neutral * 100)}%
                  </span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div
                    className="bg-gray-500 h-2 rounded-full"
                    style={{ width: `${similarityData.sentiment_analysis.article2.neutral * 100}%` }}
                  ></div>
                </div>
                
                <div className="flex justify-between items-center">
                  <span className="text-sm text-gray-600">Negative</span>
                  <span className="text-sm font-medium text-red-600">
                    {Math.round(similarityData.sentiment_analysis.article2.negative * 100)}%
                  </span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div
                    className="bg-red-500 h-2 rounded-full"
                    style={{ width: `${similarityData.sentiment_analysis.article2.negative * 100}%` }}
                  ></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Detailed Entity and Keyword Analysis */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h3 className="text-xl font-bold text-gray-900 mb-4">
          Detailed Analysis Summary
        </h3>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <h4 className="font-semibold text-gray-900 mb-3">Entity Analysis</h4>
            <div className="space-y-3">
              <div>
                <span className="text-sm font-medium text-gray-600">Common Entities:</span>
                <div className="mt-1 flex flex-wrap gap-1">
                  {similarityData.common_entities.map((entity, index) => (
                    <span
                      key={index}
                      className="inline-flex items-center px-2 py-1 rounded text-xs font-medium bg-green-100 text-green-800"
                    >
                      {entity}
                    </span>
                  ))}
                </div>
              </div>
              
              <div>
                <span className="text-sm font-medium text-gray-600">Unique to Article 1:</span>
                <div className="mt-1 flex flex-wrap gap-1">
                  {similarityData.different_entities.article1.map((entity, index) => (
                    <span
                      key={index}
                      className="inline-flex items-center px-2 py-1 rounded text-xs font-medium bg-orange-100 text-orange-800"
                    >
                      {entity}
                    </span>
                  ))}
                </div>
              </div>
              
              <div>
                <span className="text-sm font-medium text-gray-600">Unique to Article 2:</span>
                <div className="mt-1 flex flex-wrap gap-1">
                  {similarityData.different_entities.article2.map((entity, index) => (
                    <span
                      key={index}
                      className="inline-flex items-center px-2 py-1 rounded text-xs font-medium bg-red-100 text-red-800"
                    >
                      {entity}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          </div>

          <div>
            <h4 className="font-semibold text-gray-900 mb-3">Keyword Analysis</h4>
            <div className="space-y-3">
              <div>
                <span className="text-sm font-medium text-gray-600">Common Keywords:</span>
                <div className="mt-1 flex flex-wrap gap-1">
                  {similarityData.common_keywords.map((keyword, index) => (
                    <span
                      key={index}
                      className="inline-flex items-center px-2 py-1 rounded text-xs font-medium bg-blue-100 text-blue-800"
                    >
                      {keyword}
                    </span>
                  ))}
                </div>
              </div>
              
              <div>
                <span className="text-sm font-medium text-gray-600">Unique to Article 1:</span>
                <div className="mt-1 flex flex-wrap gap-1">
                  {similarityData.different_keywords.article1.map((keyword, index) => (
                    <span
                      key={index}
                      className="inline-flex items-center px-2 py-1 rounded text-xs font-medium bg-purple-100 text-purple-800"
                    >
                      {keyword}
                    </span>
                  ))}
                </div>
              </div>
              
              <div>
                <span className="text-sm font-medium text-gray-600">Unique to Article 2:</span>
                <div className="mt-1 flex flex-wrap gap-1">
                  {similarityData.different_keywords.article2.map((keyword, index) => (
                    <span
                      key={index}
                      className="inline-flex items-center px-2 py-1 rounded text-xs font-medium bg-pink-100 text-pink-800"
                    >
                      {keyword}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SimilarityAnalysis;
