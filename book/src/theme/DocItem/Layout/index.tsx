import React from 'react';
import Layout from '@theme-original/DocItem/Layout';
import type LayoutType from '@theme/DocItem/Layout';
import type {WrapperProps} from '@docusaurus/types';
import PersonalizeButton from '@site/src/components/PersonalizeButton/PersonalizeButton';

type Props = WrapperProps<typeof LayoutType>;

export default function LayoutWrapper(props: Props): JSX.Element {
  const [chapterTitle, setChapterTitle] = React.useState('');
  const [chapterContent, setChapterContent] = React.useState('');

  React.useEffect(() => {
    // Extract title from h1 element
    const h1Element = document.querySelector('article h1');
    if (h1Element) {
      setChapterTitle(h1Element.textContent || '');
    }

    // Extract content from the article element
    const articleElement = document.querySelector('article');
    if (articleElement) {
      setChapterContent(articleElement.textContent || '');
    }
  }, []);

  return (
    <>
      <Layout {...props} />
      {/* Add personalization button after the main content */}
      {chapterTitle && (
        <div style={{ marginTop: '2rem', marginBottom: '2rem' }}>
          <PersonalizeButton
            chapterTitle={chapterTitle}
            chapterContent={chapterContent}
          />
        </div>
      )}
    </>
  );
}
