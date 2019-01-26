package extractWikiJava;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.PrintStream;
import java.io.UnsupportedEncodingException;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import info.bliki.wiki.dump.IArticleFilter;
import info.bliki.wiki.dump.Siteinfo;
import info.bliki.wiki.dump.WikiArticle;
import info.bliki.wiki.dump.WikiXMLParser;
import info.bliki.wiki.filter.PlainTextConverter;
import info.bliki.wiki.model.WikiModel;

import org.apache.commons.lang3.StringUtils;
import org.xml.sax.SAXException;

public class wikiParseAleckej {

	/**
	 * @param args
	 * @throws SAXException
	 * @throws IOException
	 * @throws SAXException
	 * @throws ParserConfigurationException
	 */
	public static void main(String[] args) throws IOException, SAXException {

		String dumpfile = "E:\\Downloads\\rowiki-latest-pages-articles.xml";
		File file = new File(dumpfile);

		IArticleFilter handler = new ArticleFilter();
		WikiXMLParser wxp = new WikiXMLParser(file, handler);

		wxp.parse();

	}

	/**
	 * Print title an content of all the wiki pages in the dump.
	 * 
	 */
	static class ArticleFilter implements IArticleFilter {

		final static Pattern regex = Pattern.compile("[A-Z][\\p{L}\\w\\p{Blank},\\\"\\';\\[\\]\\(\\)-]+[\\.!]",
				Pattern.CANON_EQ);

		// Convert to plain text
		WikiModel wikiModel = new WikiModel("${image}", "${title}");
		PrintStream out = null;
		
		public ArticleFilter() {
			try {
				out = new PrintStream("F:\\Anul3semI\\IA\\Proiect\\output.txt", "UTF-8");
			}
			catch (Exception e)
			{
				System.out.println(e.getMessage());
			}
		}

		public void process(WikiArticle page, Siteinfo siteinfo) throws IOException {

			if (page != null && page.getText() != null && !page.getText().startsWith("#REDIRECT ")) {

				// Zap headings ==some text== or ===some text===

				// <ref>{{Cite web|url=http://tmh.floonet.net/articles/falseprinciple.html
				// |title="The False Principle of our Education" by Max Stirner
				// |publisher=Tmh.floonet.net |date= |accessdate=2010-09-20}}</ref>
				// <ref>Christopher Gray, ''Leaving the Twentieth Century'', p. 88.</ref>
				// <ref>Sochen, June. 1972. ''The New Woman: Feminism in Greenwich Village
				// 1910Ð1920.'' New York: Quadrangle.</ref>

				// String refexp = "[A-Za-z0-9+\\s\\{\\}:_=''|\\.\\w#\"\\(\\)\\[\\]/,?&%Ð-]+";

				String wikiText = page.getText().replaceAll("[=]+[A-Za-z+\\s-]+[=]+", " ")
						.replaceAll("\\{\\{[A-Za-z0-9+\\s-]+\\}\\}", " ").replaceAll("(?m)<ref>.+</ref>", " ")
						.replaceAll("(?m)<ref name=\"[A-Za-z0-9\\s-]+\">.+</ref>", " ").replaceAll("<ref>", " <ref>");

				// Remove text inside {{ }}
				String plainStr = wikiModel.render(new PlainTextConverter(), wikiText)
						.replaceAll("\\{\\{[A-Za-z+\\s-]+\\}\\}", " ");

				Matcher regexMatcher = regex.matcher(plainStr);
				while (regexMatcher.find()) {
					// Get sentences with 6 or more words
					String sentence = regexMatcher.group();

					if (matchSpaces(sentence, 5)) {
						out.println(sentence.toLowerCase().replaceAll("[^a-zA-Z0-9ăîâșț ]", ""));
						out.flush();
					}
				}

			}
		}

		private boolean matchSpaces(String sentence, int matches) {

			int c = 0;
			for (int i = 0; i < sentence.length(); i++) {
				if (sentence.charAt(i) == ' ')
					c++;
				if (c == matches)
					return true;
			}
			return false;
		}

	}

}