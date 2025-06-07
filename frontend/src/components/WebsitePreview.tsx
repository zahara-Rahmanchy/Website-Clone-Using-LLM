'use client';

type Props = {
  html: string;
};

export default function WebsitePreview({ html }: Props) {
  return (
    <iframe
      srcDoc={html}
      className="w-[90%] h-[80vh] mx-auto border rounded-lg scroll-auto bg-neutral-50 dark:bg-neutral-800"
      sandbox="allow-same-origin allow-scripts allow-popups"
    //   frameBorder="0"
      scrolling="auto"
      // style={{ width: '100%', height: '80vh' }}
      title="Cloned Website Preview"
    />
  );
}
