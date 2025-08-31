import React, { useState, useEffect } from 'react';
import { ArrowLeftRight, BarChart3 } from 'lucide-react';

const Comparison = ({ newsData, onSimilarityAnalysis }) => {
  const [articles, setArticles] = useState([]);
  const [selectedArticles, setSelectedArticles] = useState([]);
  const [comparisonResult, setComparisonResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    if (newsData && newsData.articles) {
      setArticles(newsData.articles);
    } else {
      // Mock data for demonstration
      setArticles([
        {
          id: 1,
          title: 'Political Development in Thailand',
          source: 'Bangkok Post',
          date: '2024-01-15',
          content: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua...',
          url: 'https://example.com/article1'
        },
        {
          id: 2,
          title: 'Thailand Political Update',
          source: 'The Nation',
          date: '2024-01-15',
          content: 'Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat...',
          url: 'https://example.com/article2'
        },
        {
          id: 3,
          title: 'Government Policy Changes',
          source: 'Thai PBS',
          date: '2024-01-16',
          content: 'Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur...',
          url: 'https://example.com/article3'
        }
      ]);
    }
  }, [newsData]);

  const handleArticleSelection = (articleId) => {
    setSelectedArticles(prev => {
      const isSelected = prev.includes(articleId);
      if (isSelected) {
        return prev.filter(id => id !== articleId);
      } else if (prev.length < 2) {
        return [...prev, articleId];
      } else {
        return [prev[1], articleId]; // Replace first with new selection
      }
    });
  };

  const compareArticles = async () => {
    if (selectedArticles.length !== 2) return;

    setIsLoading(true);
    try {
      // Mock comparison API call
      const mockComparison = {
        similarity_score: 0.75,
        common_entities: ['Person A', 'Organization B', 'Bangkok'],
        different_entities: {
          article1: ['Minister X', 'Policy Y'],
          article2: ['Official Z', 'Initiative W']
        },
        common_keywords: ['government', 'policy', 'Thailand', 'development'],
        different_keywords: {
          article1: ['reform', 'implementation'],
          article2: ['change', 'approval']
        },
        sentiment_analysis: {
          article1: { positive: 0.6, neutral: 0.3, negative: 0.1 },
          article2: { positive: 0.4, neutral: 0.4, negative: 0.2 }
        },
        content_differences: [
          {
            type: 'added',
            text: 'This content appears only in Article 2',
            article: 2
          },
          {
            type: 'removed',
            text: 'This content appears only in Article 1',
            article: 1
          }
        ]
      };

      setComparisonResult(mockComparison);
      onSimilarityAnalysis(mockComparison);
    } catch (error) {
      console.error('Error comparing articles:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const getSelectedArticle = (index) => {
    if (selectedArticles.length > index) {
      return articles.find(article => article.id === selectedArticles[index]);
    }
    return null;
  };

  return (
    <div className="space-y-6">
      {/* Article Selection */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-4">
          Select Articles for Comparison
        </h2>
        <p className="text-gray-600 mb-4">
          Choose up to 2 articles to compare their content, entities, and perspectives.
        </p>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {articles.map((article) => (
            <div
              key={article.id}
              className={`border rounded-lg p-4 cursor-pointer transition-all ${
                selectedArticles.includes(article.id)
                  ? 'border-blue-500 bg-blue-50 shadow-md'
                  : 'border-gray-200 hover:border-gray-300 hover:shadow-sm'
              }`}
              onClick={() => handleArticleSelection(article.id)}
            >
              <div className="flex justify-between items-start mb-2">
                <h3 className="text-lg font-semibold text-gray-900 line-clamp-2">
                  {article.title}
                </h3>
                {selectedArticles.includes(article.id) && (
                  <span className="ml-2 inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                    Selected
                  </span>
                )}
              </div>
              <p className="text-sm text-gray-600 mb-2">
                {article.source} • {article.date}
              </p>
              <p className="text-gray-700 text-sm line-clamp-3">
                {article.content}
              </p>
            </div>
          ))}
        </div>

        {selectedArticles.length === 2 && (
          <div className="mt-6 flex justify-center">
            <button
              onClick={compareArticles}
              disabled={isLoading}
              className="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50"
            >
              {isLoading ? (
                <>
                  <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Comparing...
                </>
              ) : (
                <>
                  <ArrowLeftRight className="h-5 w-5 mr-2" />
                  Compare Articles
                </>
              )}
            </button>
          </div>
        )}
      </div>

      {/* Comparison Results */}
      {comparisonResult && (
        <div className="space-y-6">
          {/* Similarity Overview */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-xl font-bold text-gray-900">
                Similarity Analysis
              </h3>
              <div className="flex items-center">
                <BarChart3 className="h-5 w-5 text-blue-600 mr-2" />
                <span className="text-2xl font-bold text-blue-600">
                  {Math.round(comparisonResult.similarity_score * 100)}%
                </span>
              </div>
            </div>
            
            <div className="w-full bg-gray-200 rounded-full h-3 mb-4">
              <div
                className="bg-blue-600 h-3 rounded-full"
                style={{ width: `${comparisonResult.similarity_score * 100}%` }}
              ></div>
            </div>
            
            <p className="text-gray-600">
              The articles share {Math.round(comparisonResult.similarity_score * 100)}% similarity in content and themes.
            </p>
          </div>

          {/* Side-by-side Comparison */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h3 className="text-xl font-bold text-gray-900 mb-4">
              Article Comparison
            </h3>
            <div className="grid grid-cols-2 gap-6">
              {[0, 1].map((index) => {
                const article = getSelectedArticle(index);
                return article ? (
                  <div key={index} className="space-y-4">
                    <h4 className="text-lg font-semibold text-gray-900">
                      {article.title}
                    </h4>
                    <p className="text-sm text-gray-600">
                      {article.source} • {article.date}
                    </p>
                    <div className="prose prose-sm max-w-none">
                      <p className="text-gray-700">{article.content}</p>
                    </div>
                  </div>
                ) : null;
              })}
            </div>
          </div>

          {/* Entities and Keywords Comparison */}
          <div className="grid grid-cols-2 gap-6">
            {/* Common Elements */}
            <div className="bg-white rounded-lg shadow-md p-6">
              <h3 className="text-xl font-bold text-gray-900 mb-4">
                Common Elements
              </h3>
              
              <div className="space-y-4">
                <div>
                  <h4 className="font-semibold text-gray-900 mb-2">Entities</h4>
                  <div className="flex flex-wrap gap-2">
                    {comparisonResult.common_entities.map((entity, index) => (
                      <span
                        key={index}
                        className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800"
                      >
                        {entity}
                      </span>
                    ))}
                  </div>
                </div>
                
                <div>
                  <h4 className="font-semibold text-gray-900 mb-2">Keywords</h4>
                  <div className="flex flex-wrap gap-2">
                    {comparisonResult.common_keywords.map((keyword, index) => (
                      <span
                        key={index}
                        className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800"
                      >
                        {keyword}
                      </span>
                    ))}
                  </div>
                </div>
              </div>
            </div>

            {/* Different Elements */}
            <div className="bg-white rounded-lg shadow-md p-6">
              <h3 className="text-xl font-bold text-gray-900 mb-4">
                Unique Elements
              </h3>
              
              <div className="space-y-4">
                <div>
                  <h4 className="font-semibold text-gray-900 mb-2">Article 1 Only</h4>
                  <div className="flex flex-wrap gap-2 mb-3">
                    {comparisonResult.different_entities.article1.map((entity, index) => (
                      <span
                        key={index}
                        className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-orange-100 text-orange-800"
                      >
                        {entity}
                      </span>
                    ))}
                  </div>
                  <div className="flex flex-wrap gap-2">
                    {comparisonResult.different_keywords.article1.map((keyword, index) => (
                      <span
                        key={index}
                        className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-purple-100 text-purple-800"
                      >
                        {keyword}
                      </span>
                    ))}
                  </div>
                </div>
                
                <div>
                  <h4 className="font-semibold text-gray-900 mb-2">Article 2 Only</h4>
                  <div className="flex flex-wrap gap-2 mb-3">
                    {comparisonResult.different_entities.article2.map((entity, index) => (
                      <span
                        key={index}
                        className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-800"
                      >
                        {entity}
                      </span>
                    ))}
                  </div>
                  <div className="flex flex-wrap gap-2">
                    {comparisonResult.different_keywords.article2.map((keyword, index) => (
                      <span
                        key={index}
                        className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-pink-100 text-pink-800"
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
      )}
    </div>
  );
};

export default Comparison;
