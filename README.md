# WikiRefToMdRef
Automatic processing of image linking issues when transitioning from Joplin to Obsidian.



# Why did this tool come into being?

When I use this tool "[https://github.com/luxi78/joplin2obsidian](https://github.com/luxi78/joplin2obsidian)" to transfer my notes from Joplin to Obsidian, I find a problem in image reference link. Due to Joplin putting all the pictures in one folder, it was difficult to extract a part of the notes separately. Therefore, I wrote a tool for separating them.



# About my note organization format

I usually use folders to organize my note files, and the nesting of folders is like a tree. For image management, I usually create a folder called "assets" in the same level directory as the ".md" file, and then create a folder within this folder with the same file name as the ".md" file to store the images. I think this is a pretty good way to manage images because it makes it easy for me to share and transfer my notes and images separately.

They're like this below.

```text
notes
│  note1.md
│  note2.md
└─assets
  ├─note1
  |	 image1.png
  |	 image2.png
  └─note2
  	 image1.png
  	 image2.png
```

I usually only use `![[]]` double chain syntax in ".md" file.
