import React, { useState } from 'react';
import './App.css';
import NewsInput from './components/NewsInput';
import Timeline from './components/Timeline';
import Comparison from './components/Comparison';
import SimilarityAnalysis from './components/SimilarityAnalysis';

function App() {
  const [currentView, setCurrentView] = useState('input');
  const [newsData, setNewsData] = useState(null);
  const [timelineData, setTimelineData] = useState(null);
  const [similarityData, setSimilarityData] = useState(null);

  const handleNewsAnalysis = (data) => {
    setNewsData(data);
    setCurrentView('timeline');
  };

  const handleTimelineGenerated = (data) => {
    setTimelineData(data);
  };

  const handleSimilarityAnalysis = (data) => {
    setSimilarityData(data);
  };

  const renderCurrentView = () => {
    switch (currentView) {
      case 'input':
        return <NewsInput onAnalysisComplete={handleNewsAnalysis} />;
      case 'timeline':
        return (
          <Timeline 
            newsData={newsData} 
            onTimelineGenerated={handleTimelineGenerated}
          />
        );
      case 'comparison':
        return (
          <Comparison 
            newsData={newsData}
            onSimilarityAnalysis={handleSimilarityAnalysis}
          />
        );
      case 'similarity':
        return (
          <SimilarityAnalysis 
            similarityData={similarityData}
          />
        );
      default:
        return <NewsInput onAnalysisComplete={handleNewsAnalysis} />;
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <h1 className="text-2xl font-bold text-gray-900">
              NewsTimelineAI
            </h1>
            <p className="text-gray-600">
              Automatic News Timeline and Similarity Analysis
            </p>
          </div>
        </div>
      </header>

      {/* Navigation */}
      <nav className="bg-white border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex space-x-8">
            {[
              { id: 'input', label: 'News Input' },
              { id: 'timeline', label: 'Timeline' },
              { id: 'comparison', label: 'Comparison' },
              { id: 'similarity', label: 'Similarity Analysis' }
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() => setCurrentView(tab.id)}
                className={`py-4 px-1 border-b-2 font-medium text-sm ${
                  currentView === tab.id
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                {tab.label}
              </button>
            ))}
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        {renderCurrentView()}
      </main>
    </div>
  );
}

export default App;
